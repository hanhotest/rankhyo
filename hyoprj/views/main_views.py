from flask import Blueprint,jsonify,request,render_template
from hyoprj.models import Rank
from datetime import datetime
from hyoprj import db
import uuid

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/rank_insert', methods=['POST'])
def rank_insert():
    # request에서 데이터 추출
    data = request.get_json()

    # 필수 값 체크
    uuid_ = data.get('uuid')
    userid = data.get('userid')
    usertype = data.get('usertype')
    score = data.get('score')

    if not userid or score is None:
        return jsonify({"error": "Missing userid or score"}), 400
        
    if uuid_!='':    
        user_rank = Rank.query.get(uuid_)
        user_rank.score = score
        user_rank.create_date=datetime.now()
        db.session.commit()
        return jsonify({"result": '성공!'}), 201
    
    elif uuid_=='' or usertype=='2':
        try:
            # Rank 객체 생성
            uuiddata = str(uuid.uuid1())
            print(uuiddata)
            new_rank = Rank(
                id = uuiddata,
                userid=userid,
                usertype=usertype,
                score=score,
                create_date=datetime.now()  # 현재 시간으로 설정
            )
            
            
            print(new_rank.id)
            

            # 데이터베이스에 추가
            db.session.add(new_rank)
            db.session.commit()
            
            
            user_rank = Rank.query.order_by(Rank.score.desc()).filter(Rank.score > new_rank.score).count() + 1
            
            

            return jsonify({"uuid": new_rank.id  , "rank":user_rank}), 201
        except Exception as e:
            db.session.rollback()  # 오류 시 롤백
            return jsonify({"error": str(e)}), 500
        



# 랭킹 리스트를 점수 내림차순으로 보여주는 API
@bp.route('/rank_list', methods=['GET'])
def rank_list():
    try:
        # 점수 내림차순으로 Rank 테이블에서 데이터를 조회
        rank_list = Rank.query.order_by(Rank.score.desc()).all()

        # 결과를 JSON으로 변환
        result = [
            {
                "userid": rank.userid,
                "score": rank.score,
                "create_date": rank.create_date
            } for rank in rank_list[0:5]
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500