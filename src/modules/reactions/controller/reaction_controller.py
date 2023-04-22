from flask import Blueprint
from flask_cors import cross_origin
from flask_pydantic import validate
from pydantic import BaseModel

from src.modules.reactions.model.reaction_model import Reaction
from src.modules.users.model.token_data import UserTokenData
from src.shared.utils.auth.tokenized_decorator import tokenized

reaction_controller = Blueprint("reactions", __name__, url_prefix="/reactions")


class SetReactionRequest(BaseModel):
    video_id: str


@reaction_controller.route("/create", methods=["POST"])
@cross_origin(supports_credentials=True)
@tokenized()
@validate(body=SetReactionRequest)
def set_reaction(token_data: UserTokenData, body: SetReactionRequest):
    Reaction.create(user_id=token_data.id, video_id=body.video_id).save()
    return "ok", 200
