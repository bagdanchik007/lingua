from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.progress import UserProgress, ExerciseResult
from app.models.vocabulary import UserVocabulary
from app.schemas.progress import ExerciseSubmit, UserStats


def submit_exercise(db: Session, user_id: int, data: ExerciseSubmit) -> ExerciseResult:
    result = ExerciseResult(
        user_id=user_id,
        grammar_topic_id=data.grammar_topic_id,
        vocabulary_id=data.vocabulary_id,
        exercise_type=data.exercise_type,
        is_correct=data.is_correct,
        user_answer=data.user_answer,
        correct_answer=data.correct_answer,
    )
    db.add(result)

    # Progress aktualisieren falls Grammar Topic
    if data.grammar_topic_id:
        progress = (
            db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id,
                UserProgress.grammar_topic_id == data.grammar_topic_id,
            )
            .first()
        )
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                language_id=0,  # wird später korrekt gesetzt
                grammar_topic_id=data.grammar_topic_id,
                status="in_progress",
                started_at=datetime.now(timezone.utc),
            )
            db.add(progress)

        progress.exercises_done += 1
        if data.is_correct:
            progress.exercises_correct += 1
        if progress.exercises_done > 0:
            progress.progress_percent = (progress.exercises_correct / progress.exercises_done) * 100

    db.commit()
    db.refresh(result)
    return result


def get_user_stats(db: Session, user_id: int) -> UserStats:
    total = db.query(func.count(ExerciseResult.id)).filter(ExerciseResult.user_id == user_id).scalar() or 0
    correct = (
        db.query(func.count(ExerciseResult.id))
        .filter(ExerciseResult.user_id == user_id, ExerciseResult.is_correct == True)
        .scalar()
        or 0
    )
    vocab_learned = (
        db.query(func.count(UserVocabulary.id))
        .filter(UserVocabulary.user_id == user_id, UserVocabulary.repetitions >= 3)
        .scalar()
        or 0
    )
    grammar_completed = (
        db.query(func.count(UserProgress.id))
        .filter(UserProgress.user_id == user_id, UserProgress.status == "completed")
        .scalar()
        or 0
    )

    accuracy = (correct / total * 100) if total > 0 else 0.0

    return UserStats(
        total_exercises=total,
        correct_exercises=correct,
        accuracy=round(accuracy, 1),
        vocabulary_learned=vocab_learned,
        grammar_topics_completed=grammar_completed,
        current_streak=0,
    )
