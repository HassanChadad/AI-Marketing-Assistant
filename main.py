# main.py

from harness.state import ContentState
from agents.blog_writer import write_blog_draft
from agents.orchestrator import orchestrate_review
from agents.seo_agent import select_keyword
from agents.visual_brief_agent import generate_visual_brief
from tools.content_history_store import retrieve_similar_drafts, store_draft

def run_content_loop(topic: str, platform: str = "blog"):
    keyword = select_keyword(topic)
    print(f"Selected SEO keyword: {keyword}\n")

    examples = retrieve_similar_drafts(topic, platform)
    print(f"Found {len(examples)} similar past draft(s) to use as examples\n")

    state = ContentState(topic)
    feedback = None

    while not state.is_maxed_out():
        draft = write_blog_draft(state.topic, platform=platform, keyword=keyword,
                                  feedback=feedback, examples=examples)

        result = orchestrate_review(draft, keyword, platform=platform)
        state.add_draft(draft, score=result["score"])

        print(f"\n--- Draft {state.revision_count} (score: {result['score']}%) ---\n{draft}\n")
        print(f"Orchestrator verdict: {result['verdict']}")
        print(f"Orchestrator feedback: {result['feedback']}")

        if result["verdict"] == "GOOD":
            print("Loop decided: good enough, stopping.")
            break

        feedback = result["feedback"]

    if state.is_maxed_out():
        print(f"\nLoop hit max revisions. Best draft scored {state.best_score}%.")

    final_draft = state.best_draft

    store_draft(topic, platform, final_draft)

    visual_brief = generate_visual_brief(topic, platform=platform)
    print(f"\n--- Visual Brief ---\n{visual_brief}\n")

    return final_draft, visual_brief


if __name__ == "__main__":
    final_text, brief = run_content_loop(
        topic="local LLMs for content creation",
        platform="blog"
    )
    print("\n=== FINAL DRAFT ===\n")
    print(final_text)
    print("\n=== VISUAL BRIEF ===\n")
    print(brief)