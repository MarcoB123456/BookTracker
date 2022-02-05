def build_rating(rating):
    if rating is None:
        return ""
    else:
        return "★" * rating + "☆" * (5 - rating)