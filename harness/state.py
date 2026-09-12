from harness.config import MAX_REVISIONS

class ContentState:
    def __init__(self, topic: str, max_revisions: int = MAX_REVISIONS):
        self.topic = topic
        self.drafts: list[str] = []
        self.revision_count = 0
        self.max_revisions = max_revisions
        self.best_draft = None
        self.best_score = -1

    def add_draft(self, draft: str, score: int = None):
        self.drafts.append(draft)
        self.revision_count += 1
        if score is not None and score >= self.best_score:  # >= so latest wins ties
            self.best_score = score
            self.best_draft = draft

    def is_maxed_out(self) -> bool:
        return self.revision_count >= self.max_revisions

    def latest_draft(self) -> str:
        return self.drafts[-1] if self.drafts else None

    def best_draft(self) -> str:
        return self.best_draft