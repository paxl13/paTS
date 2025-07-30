"""Resume command for paTS"""

from pats.database import get_previous_session, start_new_session


def resume():
    """Resume tracking time for last tracked project."""

    previous_session = get_previous_session()
    if previous_session:
        start_new_session(
            previous_session["project"] or "", previous_session["description"] or ""
        )
