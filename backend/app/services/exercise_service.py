from sqlalchemy.orm import Session

from app.models.exercise import Exercise
from app.models.progress import ExerciseResult
from app.schemas.exercise import ExerciseCreate, ExerciseAnswer, ExerciseCheckResult
from app.utils.exceptions import NotFoundError
from app.core.constants import EXERCISE_TYPES


def create_exercise(db: Session, data: ExerciseCreate) -> Exercise:
    if data.exercise_type not in EXERCISE_TYPES:
        # trotzdem erlauben für Erweiterbarkeit, aber logisch ok
        pass
    ex = Exercise(**data.model_dump())
    db.add(ex)
    db.commit()
    db.refresh(ex)
    return ex


def list_exercises(
    db: Session,
    language_id: int | None = None,
    level_id: int | None = None,
    grammar_topic_id: int | None = None,
    exercise_type: str | None = None,
    limit: int = 20,
):
    q = db.query(Exercise).filter(Exercise.is_active == True)
    if language_id:
        q = q.filter(Exercise.language_id == language_id)
    if level_id:
        q = q.filter(Exercise.level_id == level_id)
    if grammar_topic_id:
        q = q.filter(Exercise.grammar_topic_id == grammar_topic_id)
    if exercise_type:
        q = q.filter(Exercise.exercise_type == exercise_type)
    return q.limit(limit).all()


def get_exercise(db: Session, exercise_id: int) -> Exercise:
    ex = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.is_active == True).first()
    if not ex:
        raise NotFoundError("Exercise not found")
    return ex


def check_answer(db: Session, user_id: int, payload: ExerciseAnswer) -> ExerciseCheckResult:
    ex = get_exercise(db, payload.exercise_id)
    user_ans = (payload.user_answer or "").strip().lower()
    correct = (ex.correct_answer or "").strip().lower()
    is_correct = user_ans == correct

    result = ExerciseResult(
        user_id=user_id,
        grammar_topic_id=ex.grammar_topic_id,
        vocabulary_id=ex.vocabulary_id,
        exercise_type=ex.exercise_type,
        is_correct=is_correct,
        user_answer=payload.user_answer,
        correct_answer=ex.correct_answer,
    )
    db.add(result)
    db.commit()

    xp = 10 if is_correct else 2
    return ExerciseCheckResult(
        exercise_id=ex.id,
        is_correct=is_correct,
        correct_answer=ex.correct_answer,
        explanation=ex.explanation,
        xp_gained=xp,
    )
