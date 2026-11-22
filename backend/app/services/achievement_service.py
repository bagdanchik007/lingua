from sqlalchemy.orm import Session

from app.models.achievement import Achievement, UserAchievement
from app.models.progress import ExerciseResult
from app.models.review import UserStreak


DEFAULT_ACHIEVEMENTS = [
    {
        "code": "first_exercise",
        "title": "Erste Übung",
        "description": "Du hast deine erste Übung abgeschlossen.",
        "icon": "star",
        "xp_reward": 20,
    },
    {
        "code": "streak_3",
        "title": "3-Tage-Streak",
        "description": "Drei Tage in Folge gelernt.",
        "icon": "fire",
        "xp_reward": 50,
    },
    {
        "code": "streak_7",
        "title": "Wochen-Streak",
        "description": "Sieben Tage in Folge gelernt.",
        "icon": "fire",
        "xp_reward": 120,
    },
    {
        "code": "exercises_50",
        "title": "50 Übungen",
        "description": "Insgesamt 50 Übungen absolviert.",
        "icon": "trophy",
        "xp_reward": 100,
    },
]


def ensure_default_achievements(db: Session) -> int:
    created = 0
    for item in DEFAULT_ACHIEVEMENTS:
        exists = db.query(Achievement).filter(Achievement.code == item["code"]).first()
        if not exists:
            db.add(Achievement(**item))
            created += 1
    if created:
        db.commit()
    return created


def list_achievements(db: Session) -> list[Achievement]:
    return db.query(Achievement).filter(Achievement.is_active == True).all()


def list_user_achievements(db: Session, user_id: int) -> list[UserAchievement]:
    return (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == user_id)
        .order_by(UserAchievement.unlocked_at.desc())
        .all()
    )


def _unlock(db: Session, user_id: int, code: str) -> UserAchievement | None:
    ach = db.query(Achievement).filter(Achievement.code == code, Achievement.is_active == True).first()
    if not ach:
        return None
    exists = (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == user_id, UserAchievement.achievement_id == ach.id)
        .first()
    )
    if exists:
        return None
    row = UserAchievement(user_id=user_id, achievement_id=ach.id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def evaluate_achievements(db: Session, user_id: int) -> list[str]:
    """Prüft und schaltet passende Achievements frei. Gibt neue Codes zurück."""
    unlocked_codes: list[str] = []
    ensure_default_achievements(db)

    total_ex = db.query(ExerciseResult).filter(ExerciseResult.user_id == user_id).count()
    if total_ex >= 1:
        if _unlock(db, user_id, "first_exercise"):
            unlocked_codes.append("first_exercise")
    if total_ex >= 50:
        if _unlock(db, user_id, "exercises_50"):
            unlocked_codes.append("exercises_50")

    streak = db.query(UserStreak).filter(UserStreak.user_id == user_id).first()
    if streak:
        if streak.current_streak >= 3 and _unlock(db, user_id, "streak_3"):
            unlocked_codes.append("streak_3")
        if streak.current_streak >= 7 and _unlock(db, user_id, "streak_7"):
            unlocked_codes.append("streak_7")

    return unlocked_codes
