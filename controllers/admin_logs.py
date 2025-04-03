from flask_restful import Resource
from models import Log
from sqlalchemy.orm import Session

class AdminLogs(Resource):
    def get(self):
        with Session(bind=self._connection) as db:
            logs = db.query(Log).order_by(Log.timestamp.desc()).limit(100).all()
            return {
                'logs': [{
                    'id': log.id,
                    'user_id': log.user_id,
                    'action': log.action,
                    'timestamp': log.timestamp.isoformat()
                } for log in logs]
            }, 200