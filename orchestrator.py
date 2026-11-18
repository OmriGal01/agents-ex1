from actor import Actor
from config import MAX_ATTEMPTS
from evaluator import Evaluator
from logger import ExecutionLogger, QuestionRunLog

TECHNICAL_ERROR_MESSAGE = (
    "A technical error occurred while processing the request. Please try again. / "
    "אירעה שגיאה טכנית בעת עיבוד הבקשה. אנא נסו שוב."
)


def format_max_attempts_message(max_attempts: int) -> str:
    return (
        f"An approved response could not be generated within the maximum allowed "
        f"attempts ({max_attempts}). / "
        f"לא התקבלה תשובה מאושרת במסגרת מגבלת הניסיונות ({max_attempts})."
    )


class ChatOrchestrator:
    def __init__(
        self,
        actor: Actor,
        evaluator: Evaluator,
        logger: ExecutionLogger | None = None,
        max_attempts: int = MAX_ATTEMPTS,
    ) -> None:
        self.actor = actor
        self.evaluator = evaluator
        self.logger = logger or ExecutionLogger()
        self.max_attempts = max_attempts

    def run(
        self,
        user_question: str,
        conversation_history: list[dict[str, str]] | None = None,
        scenario_id: str = "interactive",
        injected_first_draft: str | None = None,
    ) -> str:
        """Run the Actor-Critic loop (up to max_attempts) for a single user question."""
        run_log = QuestionRunLog(
            scenario_id=scenario_id,
            user_question=user_question,
        )

        rejected_answer: str | None = None
        critic_feedback: str | None = None

        try:
            for attempt in range(1, self.max_attempts + 1):
                candidate_answer: str | None = None
                try:
                    if attempt == 1 and injected_first_draft is not None:
                        candidate_answer = injected_first_draft
                    else:
                        candidate_answer = self.actor.generate(
                            user_question=user_question,
                            conversation_history=conversation_history,
                            rejected_answer=rejected_answer,
                            critic_feedback=critic_feedback,
                        )

                    evaluation = self.evaluator.evaluate(
                        user_question=user_question,
                        candidate_answer=candidate_answer,
                        conversation_history=conversation_history,
                    )
                except Exception as exc:
                    stage = "Actor" if candidate_answer is None else "Evaluator"
                    run_log.add_attempt(
                        attempt_number=attempt,
                        candidate_answer=candidate_answer,
                        evaluator_decision="evaluation_not_completed",
                        feedback=f"{stage} technical error: {exc}",
                    )
                    run_log.final_status = "technical_error"
                    return TECHNICAL_ERROR_MESSAGE

                run_log.add_attempt(
                    attempt_number=attempt,
                    candidate_answer=candidate_answer,
                    evaluator_decision="approved" if evaluation.is_acceptable else "rejected",
                    feedback=evaluation.feedback,
                )

                if evaluation.is_acceptable:
                    run_log.final_status = "approved"
                    return candidate_answer

                rejected_answer = candidate_answer
                critic_feedback = evaluation.feedback

            run_log.final_status = "max_attempts_exceeded"
            return format_max_attempts_message(self.max_attempts)
        finally:
            self.logger.log_run(run_log)
