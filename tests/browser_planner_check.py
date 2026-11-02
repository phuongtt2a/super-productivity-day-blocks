"""Browser regression tests for Day Blocks. Tests use a fake PluginAPI; no native data is changed."""
from datetime import date
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"plugin/index.html").read_text(encoding="utf-8")
TODAY=date.today().isoformat()
TASKS=[
 {"id":"plan","title":"Prepare quarterly plan","dueDay":TODAY,"projectId":"work","isDone":False,"subTaskIds":["outline"]},
 {"id":"outline","title":"Outline slides","projectId":"work","parentId":"plan","isDone":False,"subTaskIds":[]},
 {"id":"call","title":"Call client","dueDay":TODAY,"projectId":"work","isDone":False,"subTaskIds":[]},
 {"id":"review","title":"Review design","dueDay":TODAY,"projectId":"work","isDone":False,"subTaskIds":[]}
]
HABITS=[
 {"id":"jog","title":"Go jogging","type":"StopWatch","isEnabled":True,"isOn":False,"isTrackStreaks":True,"streakMinValue":2700000,"countOnDay":{}},
 {"id":"water","title":"Drink water","type":"ClickCounter","isEnabled":True,"isTrackStreaks":True,"streakMinValue":8,"countOnDay":{}},
 {"id":"reading","title":"Read 60 minutes","type":"StopWatch","isEnabled":True,"isOn":False,"isTrackStreaks":True,"streakMinValue":3600000,"countOnDay":{TODAY:3600000}},
 {"id":"journal","title":"Journal","type":"ClickCounter","isEnabled":True,"isTrackStreaks":True,"streakMinValue":1,"countOnDay":{}}
]
API=r"""
window.__tasks=__TASKS__;
window.__habits=__HABITS__;
window.__today=__TODAY__;
window.__saved=__SAVED__;
window.__events=[];
window.__hooks={};
window.PluginAPI={
 Hooks:{
  TASK_CREATED:'taskCreated',TASK_UPDATE:'taskUpdate',TASK_COMPLETE:'taskComplete',
  TASK_DELETE:'taskDelete', DATA_CHANGED:'dataChanged', DAY_CHANGE:'dayChange',
  PERSISTED_DATA_CHANGED:'persistedDataChanged'
 },
 registerHook:(name,fn)=>window.__hooks[name]=fn,
 getTasks:async()=>window.__tasks.map(t=>({...t})),
 getAllSimpleCounters:async()=>window.__habits.map(h=>({...h,countOnDay:{...h.countOnDay}})),
 getAllProjects:async()=>[{id:'work',title:'Work'}],
 getDayContext:async()=>({todayStr:window.__today}),
 persistDataSynced:async(data,key)=>{
  window.__events.push({name:'save',key});
  window.__saved[key]=data;
 },
 loadSyncedData:async(key)=>window.__saved[key]||null,
 updateTask:async(id,patch)=>{
  Object.assign(window.__tasks.find(t=>t.id===id),patch);
  window.__events.push({name:'task',id,patch});
 },
 setCounter:async(id,value)=>{
  window.__habits.find(h=>h.id===id).countOnDay[window.__today]=value;
  window.__events.push({name:'habit',id,value});
 }
};
"""
def install(page,saved=None):
    page.goto("about:blank")
    code=API.replace("__TASKS__",json.dumps(TASKS,ensure_ascii=False)).replace(
        "__HABITS__",json.dumps(HABITS,ensure_ascii=False)).replace(
        "__TODAY__",json.dumps(TODAY)).replace("__SAVED__",json.dumps(saved or {}))
    page.evaluate(code)
    page.set_content(HTML)
    page.wait_for_selector('#timeline .block')

def session_card(page,task_id):
    return page.locator('#timeline .session').filter(has=page.locator('.session-title',has_text=task_id))

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--no-sandbox"])
    try:
        page=browser.new_page(viewport={"width":1680,"height":1024})
        install(page)
        assert page.locator('#timeline .block').count()==4
        assert page.locator('#timeline .block').evaluate_all(
            "(blocks)=>blocks.map(b=>b.dataset.dropBlock)"
        )==["morning","afternoon","evening","night"]
        assert page.locator('#unassigned [data-source-key="habit:reading"]').count()==1
        print("one-row four-column timeline and goal-met habit in unassigned: PASS")

        # Schedule a task with exact times in Morning.
        page.locator('[data-plan-key="task:plan"]').click()
        assert page.locator('#session-backdrop:not(.hidden)').count()==1
        page.locator('#exact-time').check()
        page.locator('#session-start').fill("09:00")
        page.locator('#session-end').fill("11:00")
        page.locator('#session-save').click()
        page.wait_for_selector('#timeline [data-session]')
        assert page.locator('#unassigned [data-source-key="task:plan"]').count()==0
        assert page.locator('.morning .session-title',has_text="Prepare quarterly plan").count()==1
        assert page.locator('.morning .session-meta').first.inner_text().startswith("09:00–11:00")
        print("scheduled item leaves unassigned, precise time saved: PASS")

        # Additional linked Afternoon session shares the same native ID.
        page.locator('.morning [data-copy-session]').click()
        page.locator('#session-block').select_option('afternoon')
        page.locator('#exact-time').check()
        page.locator('#session-start').fill("14:00")
        page.locator('#session-end').fill("15:00")
        page.locator('#session-save').click()
        assert page.locator('.morning .session.multi').count()==1
        assert page.locator('.afternoon .session.multi').count()==1
        assert page.locator('.linked',has_text="2 sessions").count()==2
        assert page.locator('#metrics .metric').first.inner_text().startswith("1")
        assert page.locator('#unassigned [data-source-key="task:plan"]').count()==0
        print("same task planned twice, linked but counted once: PASS")

        # The parent task's original subtasks are available from either
        # linked session; changes update the same native subtask record.
        page.locator('.morning .subtask-panel summary').first.click()
        page.locator('.morning [data-task-done="outline"]').first.click()
        page.wait_for_function("window.__tasks.find(t=>t.id==='outline').isDone===true")
        page.locator('.afternoon .subtask-panel summary').first.click()
        assert page.locator('.afternoon .subtask-row.is-done',has_text="Outline slides").count()==1
        assert page.evaluate("window.__events.filter(e=>e.name==='task'&&e.id==='outline').length")==1
        print("subtask completion shared across linked task sessions: PASS")

        # Flexible item can be moved to the Night block; both earlier sessions remain.
        page.locator('[data-plan-key="task:call"]').click()
        page.locator('#session-block').select_option("night")
        page.locator('#exact-time').check()
        page.locator('#session-start').fill("22:30")
        page.locator('#session-end').fill("00:00")
        page.locator('#session-save').click()
        assert page.locator('.night .session-title',has_text="Call client").count()==1
        assert page.locator('.night .session-meta').first.inner_text().startswith("22:30–00:00")
        print("midnight session boundary is handled: PASS")

        # Invalid exact time shows an actionable validation error.
        page.locator('.night [data-edit-session]').click()
        page.locator('#session-block').select_option("morning")
        page.locator('#session-start').fill("17:00")
        page.locator('#session-end').fill("18:00")
        page.locator('#session-save').click()
        assert "inside Morning" in page.locator('#session-error').inner_text()
        page.locator('#session-cancel').click()
        print("invalid block time rejected: PASS")

        # A flexible 3-hour session cannot fit in the 2-hour Night block.
        page.locator('.night [data-edit-session]').click()
        page.locator('#exact-time').uncheck()
        page.locator('#session-duration').fill("180")
        page.locator('#session-save').click()
        assert "must fit Night" in page.locator('#session-error').inner_text()
        page.locator('#session-cancel').click()
        print("flexible duration respects block capacity: PASS")

        # Repeat a habit on future scheduled days.
        page.locator('[data-plan-key="habit:water"]').click()
        page.locator('#session-block').select_option("morning")
        page.locator('#session-repeat').check()
        page.locator('#session-save').click()
        page.locator('#next-day').click()
        assert page.locator('.morning .session-title',has_text="Drink water").count()==1
        assert page.locator('#unassigned [data-source-key="habit:water"]').count()==0
        # Removing from one day does not remove the future recurring preference.
        page.locator('.morning [data-remove-session]').click()
        assert page.locator('.morning .session-title',has_text="Drink water").count()==0
        page.locator('#next-day').click()
        assert page.locator('.morning .session-title',has_text="Drink water").count()==1
        page.locator('#go-today').click()
        print("recurring habit session, daily override and next-day restore: PASS")

        # A completed stopwatch habit may still be scheduled and log extra time.
        page.locator('[data-plan-key="habit:reading"]').click()
        page.locator('#session-block').select_option("evening")
        page.locator('#session-save').click()
        assert page.locator('.evening .session.is-done',has=page.locator('.session-title',has_text="Read 60 minutes")).count()==1
        page.locator('.evening [data-log-habit="reading"]').click()
        page.locator('#log-minutes').fill("30")
        page.locator('#log-save').click()
        page.wait_for_function("window.__habits.find(h=>h.id==='reading').countOnDay[window.__today]===5400000")
        assert page.locator('.evening .session.is-done',has=page.locator('.session-title',has_text="Read 60 minutes")).count()==1
        assert page.locator('#metrics .metric').first.inner_text().startswith("4")
        print("goal-met habit extra time is native, planned sessions remain independent: PASS")

        # Reorder and move individual sessions without duplicating a source item.
        page.locator('.morning [data-copy-session]').first.click()
        page.locator('#session-block').select_option("morning")
        page.locator('#session-save').click()
        all_before=page.locator('.morning [data-session]').count()
        assert all_before>=2
        second=page.locator('.morning [data-down-session]').first
        assert second.is_enabled()
        second.click()
        assert page.locator('.morning [data-session]').count()==all_before
        assert page.locator('#unassigned [data-source-key="task:plan"]').count()==0
        print("within-block reorder: PASS")

        page.wait_for_function("!!window.__saved['day-blocks.plans.v1']")
        saved=page.evaluate("window.__saved")
        data=json.loads(saved["day-blocks.plans.v1"])
        assert TODAY in data["days"]
        assert any(s["itemId"]=="plan" for s in data["days"][TODAY]["sessions"])
        assert len(data["routines"])==1
        print("synced preferences and independent session records: PASS")

        restored=browser.new_page(viewport={"width":320,"height":690},has_touch=True,is_mobile=True)
        install(restored,saved)
        assert restored.locator('.morning .session-title',has_text="Prepare quarterly plan").count()>=1
        assert restored.locator('.evening .session-title',has_text="Read 60 minutes").count()==1
        assert restored.locator('#timeline .block').count()==4
        assert restored.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
        assert restored.evaluate("document.querySelector('#timeline-scroll').scrollWidth>document.querySelector('#timeline-scroll').clientWidth")
        assert restored.evaluate("getComputedStyle(document.querySelector('#timeline')).gridAutoFlow")=="column"
        restored.locator('#unassigned [data-plan-key="task:review"]').click()
        restored.locator('#session-block').select_option("evening")
        restored.locator('#session-save').click()
        assert restored.locator('#unassigned [data-source-key="task:review"]').count()==0
        assert restored.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
        restored.close()
        print("320px mobile remains one-row scrollable, accessible Plan works: PASS")

        # Drag an unassigned item to a visible block with pointer events.
        page.locator('#unassigned [data-drag-source="task:review"]').scroll_into_view_if_needed()
        handle=page.locator('#unassigned [data-drag-source="task:review"]').bounding_box()
        destination=page.locator('.afternoon .block-list').bounding_box()
        page.mouse.move(handle['x']+handle['width']/2,handle['y']+handle['height']/2)
        page.mouse.down()
        page.mouse.move(destination['x']+destination['width']/2,destination['y']+100,steps=12)
        page.mouse.up()
        assert page.locator('.afternoon .session-title',has_text="Review design").count()==1
        assert page.locator('#unassigned [data-source-key="task:review"]').count()==0
        print("pointer drag from source into Afternoon: PASS")

        # Move that single session by drag (no duplicate), then unassign it.
        row=page.locator('.afternoon .session',has=page.locator('.session-title',has_text="Review design"))
        row.locator('[data-drag-session]').scroll_into_view_if_needed()
        handle=row.locator('[data-drag-session]').bounding_box()
        dest=page.locator('.evening .block-list').bounding_box()
        page.mouse.move(handle['x']+handle['width']/2,handle['y']+handle['height']/2)
        page.mouse.down()
        page.mouse.move(dest['x']+dest['width']/2,dest['y']+100,steps=14)
        page.mouse.up()
        assert page.locator('.evening .session-title',has_text="Review design").count()==1
        assert page.locator('.afternoon .session-title',has_text="Review design").count()==0
        assert page.locator('#unassigned [data-source-key="task:review"]').count()==0

        row=page.locator('.evening .session',has=page.locator('.session-title',has_text="Review design"))
        row.locator('[data-drag-session]').scroll_into_view_if_needed()
        handle=row.locator('[data-drag-session]').bounding_box()
        dest=page.locator('#backlog').bounding_box()
        page.mouse.move(handle['x']+handle['width']/2,handle['y']+handle['height']/2)
        page.mouse.down()
        page.mouse.move(dest['x']+dest['width']/2,dest['y']+90,steps=14)
        page.mouse.up()
        assert page.locator('.evening .session-title',has_text="Review design").count()==0
        assert page.locator('#unassigned [data-source-key="task:review"]').count()==1
        print("cross-block pointer move and drag back to Unassigned: PASS")

        # Native completion is shared across all planned sessions.
        page.locator('.afternoon [data-task-done="plan"]').click()
        page.wait_for_function("window.__tasks.find(t=>t.id==='plan').isDone===true")
        assert page.locator('.morning .session.is-done',has=page.locator('.session-title',has_text="Prepare quarterly plan")).count()>=1
        assert page.locator('.afternoon .session.is-done',has=page.locator('.session-title',has_text="Prepare quarterly plan")).count()==1
        assert page.evaluate("window.__events.filter(e=>e.name==='task'&&e.id==='plan').length")==1
        print("one native task completion updates all linked sessions: PASS")
        page.close()
    finally:
        browser.close()
