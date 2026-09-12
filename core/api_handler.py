from harness.state import ContentState
from agents.blog_writer import write_blog_draft
from agents.orchestrator import orchestrate_review
from agents.seo_agent import select_keyword
from agents.visual_brief_agent import generate_visual_brief
from tools.content_history_store import retrieve_similar_drafts, store_draft

def run_content_loop(topic: str, platform: str = "blog"):
    keyword = select_keyword(topic)
    examples = retrieve_similar_drafts(topic, platform)

    state = ContentState(topic)
    feedback = None

    while not state.is_maxed_out():
        draft = write_blog_draft(state.topic, platform=platform, keyword=keyword,
                                  feedback=feedback, examples=examples)

        result = orchestrate_review(draft, keyword, platform=platform)
        state.add_draft(draft, score=result["score"])

        if result["verdict"] == "GOOD":
            break
        feedback = result["feedback"]

    final_draft = state.best_draft
    store_draft(topic, platform, final_draft)
    visual_brief = generate_visual_brief(topic, platform=platform)

    return {
        "draft": final_draft,
        "score": state.best_score,
        "revisions": state.revision_count,
        "visual_brief": visual_brief,
        "keyword": keyword
    }