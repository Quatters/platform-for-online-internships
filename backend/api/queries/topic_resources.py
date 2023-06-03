from sqlalchemy.orm import Session
from fastapi_pagination import paginate as pypaginate
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import sort_by_self_fk, with_search
from backend.models import TopicResource


def get_topic_resources(db: Session, params: ListPageParams, topic_id: int):
    query = db.query(TopicResource).filter(TopicResource.topic_id == topic_id)
    query = with_search(TopicResource.name, query=query, search=params.search)

    resources = sort_by_self_fk(query, 'prev_resource_id')
    return pypaginate(
        resources,
        params,
        length_function=lambda _: query.count(),
    )
