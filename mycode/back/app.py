from flask import Flask, request, jsonify
# 实现跨域请求
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
# 接口
from flask.views import MethodView
from datetime import datetime
import re

from model import *

app = Flask(__name__)
# 将app绑定在CORS以实现跨域请求
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activities.sqlite'
# 数据库地址：本文件夹
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 禁止追踪
db.init_app(app)


@app.cli.command()  # 自定义指令,
def reset():
    db.drop_all()
    # 删除旧的数据表
    db.create_all()
    # 创建新的
    init_all_data()  #加入测试数据


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# Organizer 注册和登录视图
class OrganizerAPI(MethodView):
    def post(self):
        data = request.get_json()
        if request.path.endswith("/register"):
            name = data.get("name")
            password = data.get("password")
            email = data.get("email")

            if Organizer.query.filter_by(name=name).first():
                return jsonify({"message": "用户名已存在！"}), 409

            hashed_password = generate_password_hash(password)
            new_organizer = Organizer(name=name, password=hashed_password, email=email)
            db.session.add(new_organizer)
            db.session.commit()
            return jsonify({"message": "注册成功！"}), 201

        elif request.path.endswith("/login"):
            name = data.get("name")
            password = data.get("password")

            organizer = Organizer.query.filter_by(name=name).first()

            organizer_data = {
                'id': organizer.organizer_id,
                'name': organizer.name,
                'email': organizer.email,
                'compliance_status': organizer.compliance_status
            }
            if organizer and check_password_hash(organizer.password, password):
                return jsonify({"message": "登录成功！",
                                "data": organizer_data}), 200
            else:
                return jsonify({"message": "用户名或密码错误"}), 401


# Manager 注册和登录视图
class ManagerAPI(MethodView):
    def post(self):
        data = request.get_json()
        if request.path.endswith("/register"):
            name = data.get("name")
            password = data.get("password")
            email = data.get("email")

            if Manager.query.filter_by(name=name).first():
                return jsonify({"message": "用户名已存在！"}), 409

            hashed_password = generate_password_hash(password)
            new_manager = Manager(name=name, password=hashed_password, email=email)
            db.session.add(new_manager)
            db.session.commit()
            return jsonify({"message": "管理员注册成功！"}), 201

        elif request.path.endswith("/login"):
            name = data.get("name")
            password = data.get("password")

            manager = Manager.query.filter_by(name=name).first()
            manager_data = {
                'id': manager.manager_id,
                'name': manager.name,
                'email': manager.email
            }
            if manager and check_password_hash(manager.password, password):
                return jsonify({"message": "登录成功！",
                                "data": manager_data}), 200
            else:
                return jsonify({"message": "用户名或密码错误"}), 401


# Visitor 注册和登录视图
class VisitorAPI(MethodView):
    def post(self):
        data = request.get_json()
        if request.path.endswith("/register"):
            name = data.get("name")
            password = data.get("password")
            email = data.get("email")
            favorite_activity_type = data.get("favorite_activity_type")

            if Visitor.query.filter_by(name=name).first():
                return jsonify({"message": "用户名已存在！"}), 409

            hashed_password = generate_password_hash(password)
            new_visitor = Visitor(name=name, password=hashed_password, email=email,
                                  favorite_activity_type=favorite_activity_type)
            db.session.add(new_visitor)
            db.session.commit()
            return jsonify({"message": "游客注册成功！"}), 201

        elif request.path.endswith("/login"):
            name = data.get("name")
            password = data.get("password")

            visitor = Visitor.query.filter_by(name=name).first()
            visitor_data = {
                'id': visitor.visitor_id,
                'name': visitor.name,
                'email': visitor.email,
                'favorite_activity_type': visitor.favorite_activity_type
            }
            if visitor and check_password_hash(visitor.password, password):
                return jsonify({"message": "登录成功！",
                                "data": visitor_data}), 200
            else:
                return jsonify({"message": "用户名或密码错误"}), 401


# 为 Organizer、Manager、Visitor 注册 URL 路由
organizer_view = OrganizerAPI.as_view('organizer_api')
app.add_url_rule('/organizer/register', view_func=organizer_view, methods=['POST'])
app.add_url_rule('/organizer/login', view_func=organizer_view, methods=['POST'])

manager_view = ManagerAPI.as_view('manager_api')
app.add_url_rule('/manager/register', view_func=manager_view, methods=['POST'])
app.add_url_rule('/manager/login', view_func=manager_view, methods=['POST'])

visitor_view = VisitorAPI.as_view('visitor_api')
app.add_url_rule('/visitor/register', view_func=visitor_view, methods=['POST'])
app.add_url_rule('/visitor/login', view_func=visitor_view, methods=['POST'])


class VenueAPI(MethodView):
    def get(self):
        try:
            # 添加调试信息
            print("Accessing /venues endpoint")

            # 查询所有场所
            venues = Venue.query.all()
            print(f"Found {len(venues)} venues")  # 调试信息

            if not venues:
                return jsonify({"message": "No venues found"}), 500

            # 提取场所信息
            venue_list = []
            for venue in venues:
                venue_data = {
                    'venue_id': venue.venue_id,
                    'name': venue.name,
                    'longitude': float(venue.longitude),
                    'latitude': float(venue.latitude)
                }
                venue_list.append(venue_data)

            # 返回JSON响应
            return jsonify({
                'status': 'success',
                'count': len(venue_list),
                'data': venue_list
            }), 200

        except Exception as e:
            print(f"Error in /venues endpoint: {str(e)}")  # 调试信息
            return jsonify({'error': str(e)}), 500


# 注册视图类到URL路由
venue_view = VenueAPI.as_view('venue_api')
app.add_url_rule('/venues', view_func=venue_view, methods=['GET'])


@app.route('/venuesDetail', methods=['POST'])
def post_venues_id():
    try:
        data = request.get_json()
        venue_id = data.get("venue_id")
        
        # 添加类型转换，因为前端传来的可能是字符串
        venue_id = int(venue_id)
        
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if venue:
            # 构建返回数据
            venue_data = {
                'venue_id': venue.venue_id,
                'name': venue.name,
                'longitude': float(venue.longitude),
                'latitude': float(venue.latitude),
                'description': venue.description,
                'city': venue.city,
                'county': venue.county,
                'street': venue.street,
                'phone': venue.phone
            }
            return jsonify({
                "message": "场所信息获取成功！",
                'status': 'success',
                'data': venue_data
            }), 200
        else:
            return jsonify({"message": "未找到该场所！"}), 404
            
    except Exception as e:
        print(f"Error in venues_id: {str(e)}")  # 添加错误日志
        return jsonify({
            "message": "获取场所信息失败！",
            "error": str(e)
        }), 500


# 获取访客的搭子请求
@app.route('/visitor_buddy', methods=['POST'])
def get_visitor_buddy_requests():
    try:
        data = request.get_json()
        visitor_id = data.get("visitor_id")
        
        # 查询该访客的所有搭子请求
        buddy_requests = VisitorRequestBuddy.query.filter_by(visitor_id=visitor_id).all()
        
        # 构建返回数据
        requests_data = []
        for buddy_request in buddy_requests:
            # 获取关联的活动信息
            activity = Activity.query.get(buddy_request.activity_id)
            if activity:
                requests_data.append({
                    'activity_id': activity.activity_id,
                    'activity_name': activity.name,
                    'buddy_requirement': buddy_request.buddy_requirement,
                    'request_time': buddy_request.request_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'is_found': buddy_request.is_found
                })
        
        return jsonify({
            'status': 'success',
            'data': requests_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_visitor_buddy_requests: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '获取搭子请求失败'
        }), 500
@app.route('/changeBuddyStatus', methods=['POST'])
def change_buddy_status():
    try:
        data = request.get_json()
        visitor_id = data.get('visitor_id')
        activity_id = data.get('activity_id')
        is_found = data.get('is_found')
        
        # 参数验证
        if not all([visitor_id, activity_id, isinstance(is_found, bool)]):
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数或参数类型错误'
            }), 400
            
        # 查找对应的搭子请求记录
        buddy_request = VisitorRequestBuddy.query.filter_by(
            visitor_id=visitor_id,
            activity_id=activity_id
        ).first()
        
        if not buddy_request:
            return jsonify({
                'status': 'error',
                'message': '未找到对应的搭子请求'
            }), 500
            
        # 更新状态
        buddy_request.is_found = is_found
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '搭子状态更新成功',
            'data': {
                'visitor_id': visitor_id,
                'activity_id': activity_id,
                'is_found': is_found
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in change_buddy_status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '更新搭子状态失败'
        }), 500
# 删除搭子
@app.route('/deleteBuddy', methods=['POST'])
def delete_buddy():
    try:
        data = request.get_json()
        visitor_id = data.get('visitor_id')
        activity_id = data.get('activity_id')
        
        # 参数验证
        if not all([visitor_id, activity_id]):
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
            
        # 查找对应的搭子请求记录
        buddy_request = VisitorRequestBuddy.query.filter_by(
            visitor_id=visitor_id,
            activity_id=activity_id
        ).first()
        
        if not buddy_request:
            return jsonify({
                'status': 'error',
                'message': '未找到对应的搭子请求'
            }), 404
            
        # 删除记录
        db.session.delete(buddy_request)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '搭子请求删除成功',
            'data': {
                'visitor_id': visitor_id,
                'activity_id': activity_id
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_buddy: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '删除搭子请求失败'
        }), 500
# 获取组织者发布的活动
@app.route('/organizer_activities', methods=['POST'])
def get_organizer_activities():
    try:
        data = request.get_json()
        organizer_id = data.get("organizer_id")
        # 查询该组织者管理的所有活动
        activities = OrganizerManagesActivity.query.filter_by(organizer_id=organizer_id).all()
        
        # 构建返回数据
        activities_data = []
        for organizer_activity in activities:
            activity = Activity.query.get(organizer_activity.activity_id)
            if activity:
                thisVenue = ActivityInVenue.query.filter_by(activity_id=activity.activity_id).first()
                if(thisVenue):
                    activities_data.append({
                        'venue_id': thisVenue.venue_id,
                        'venue': Venue.query.filter_by(venue_id=thisVenue.venue_id).first().name,
                        'activity_id': activity.activity_id,
                        'name': activity.name,
                        'type': activity.type,
                        'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'end_time': activity.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'description': activity.description,
                        'flow': activity.flow
                    })
                else:
                    activities_data.append({
                        'activity_id': activity.activity_id,
                        'name': activity.name,
                        'type': activity.type,
                        'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'end_time': activity.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'description': activity.description,
                        'flow': activity.flow})
        
        return jsonify({
            'status': 'success',
            'data': activities_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_organizer_activities: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '获取活动列表失败'
        }), 500

# 获取管理员管理的组织者
@app.route('/organizers', methods=['GET'])
def get_manager_organizers():
    try:
        organizers = Organizer.query.all()
        # 构建返回数据
        organizers_data = []
        for organizer in organizers:
            organizers_data.append({
                'organizer_id': organizer.organizer_id,
                'name': organizer.name,
                'email': organizer.email,
                'compliance_status': organizer.compliance_status
            })
        return jsonify({
            'status': 'success',
            'data': organizers_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_manager_organizers: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '获取组织者列表失败'
        }), 500


# 更新组织者合规状态
@app.route('/changeOrganizerStatus', methods=['POST'])
def change_organizer_status():
    try:
        data = request.get_json()
        organizer_id = data.get('organizer_id')
        new_status = data.get('status')

        # 参数验证
        if organizer_id is None or new_status is None:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400

        # 查找组织者
        organizer = Organizer.query.get(organizer_id)
        if not organizer:
            return jsonify({
                'status': 'error',
                'message': '组织者不存在'
            }), 404

        # 更新合规状态
        organizer.compliance_status = new_status
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': '合规状态更新成功',
            'data': {
                'organizer_id': organizer_id,
                'compliance_status': new_status
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in change_organizer_status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '更新合规状态失败'
        }), 500

# 获取所有活动信息
@app.route('/activities', methods=['GET'])
def get_activities():
    try:
        activities = Activity.query.all()
        activities_data = []
        
        for activity in activities:
            # 获取活动所在场地信息
            venue = Venue.query.join(ActivityInVenue).filter(
                ActivityInVenue.activity_id == activity.activity_id
            ).first()
            
            activity_data = {
                'activity_id': activity.activity_id,
                'name': activity.name,
                'type': activity.type,
                'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': activity.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'flow': activity.flow,
                'venue_name': venue.name if venue else None,
                'registration_channel': activity.registration_channel
            }
            activities_data.append(activity_data)
            
        return jsonify({
            'status': 'success',
            'data': activities_data
        }), 200
        
    except Exception as e:
        print(f"Error in get_activities: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '获取活动列表失败'
        }), 500

# 获取活动详情、评论和搭子信息
@app.route('/activitiesDetail', methods=['POST'])
def get_activity_detail():
    try:
        data = request.get_json()
        activity_id = data.get('activity_id')
        
        if not activity_id:
            return jsonify({
                'status': 'error',
                'message': '缺少活动ID'
            }), 400
        activity_id = int(activity_id)
        # 获取活动基本信息
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({
                'status': 'error',
                'message': '活动不存在'
            }), 404
            
        # 获取活动评论
        comments = Comment.query.filter_by(activity_id=activity_id).all()
        comments_data = [{

            'content': comment.comment_content,
            'visitor_name': Visitor.query.filter_by(visitor_id=comment.visitor_id).first().name,
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        
        # 获取搭子请求
        partners = VisitorRequestBuddy.query.filter_by(activity_id=activity_id).all()
        partners_data = [{
            'visitor_name': Visitor.query.filter_by(visitor_id=partner.visitor_id).first().name,
            'email': Visitor.query.filter_by(visitor_id=partner.visitor_id).first().email,
            'requirement': partner.buddy_requirement,
            'request_time': partner.request_time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_found': partner.is_found
        } for partner in partners]
        
        # 获取场地信息
        venue = Venue.query.join(ActivityInVenue).filter(
            ActivityInVenue.activity_id == activity_id
        ).first()
        
        return jsonify({
            'status': 'success',
            'data': {
                'activity': {
                    'activity_id': activity.activity_id,
                    'name': activity.name,
                    'type': activity.type,
                    'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'end_time': activity.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'description': activity.description,
                    'flow': activity.flow,
                    'venue': venue.name if venue else None
                },
                'comments': comments_data,
                'partners': partners_data
            }
        }), 200
        
    except Exception as e:
        print(f"Error in get_activity_detail: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '获取活动详情失败'
        }), 500

def parse_datetime(datetime_str):
    """处理不同格式的日期时间字符串"""
    if not datetime_str:
        return None
        
    # 处理带T和Z的ISO格式 (例如: '2024-12-31T16:00:00.000Z')
    if 'T' in datetime_str:
        # 移除毫秒和时区信息
        datetime_str = re.sub(r'\.\d+Z$', '', datetime_str)
        # 替换T为空格
        datetime_str = datetime_str.replace('T', ' ')
        
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return None

@app.route('/addActivities', methods=['POST'])
def add_activity():
    try:
        data = request.get_json()
        
        # 使用parse_datetime函数处理日期时间
        start_time = parse_datetime(data.get('start_time'))
        end_time = parse_datetime(data.get('end_time'))
        
        if not start_time or not end_time:
            return jsonify({
                'status': 'error',
                'message': '日期时间格式错误'
            }), 400

        new_activity = Activity(
            name=data.get('name'),
            type=data.get('type'),
            start_time=start_time,
            end_time=end_time,
            description=data.get('description'),
            flow=data.get('flow')
        )
        
        db.session.add(new_activity)
        db.session.flush()
        
        # 如果提供了场地信息，创建场地关联
        if data.get('venue_id'):
            venue_relation = ActivityInVenue(
                activity_id=new_activity.activity_id,
                venue_id=data['venue_id']
            )
            db.session.add(venue_relation)
        
        # 关联组织者

        organizer_activity = OrganizerManagesActivity(
            organizer_id=data['organizer_id'],
            activity_id=new_activity.activity_id,
        )
        db.session.add(organizer_activity)
            
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '活动添加成功',
            'data': {
                'activity_id': new_activity.activity_id
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in add_activity: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '添加活动失败'
        }), 500

# 添加评论
@app.route('/addComments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        
        new_comment = Comment(
            activity_id=int(data['activity_id']),
            visitor_id=int(data['visitor_id']),
            comment_content=data['content'],
            comment_time=datetime.now()
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '评论添加成功',
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in add_comment: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '添加评论失败'
        }), 500

# 添加搭子请求
@app.route('/addPartners', methods=['POST'])
def add_partner():
    try:
        data = request.get_json()
        
        new_partner = VisitorRequestBuddy(
            activity_id=int(data['activity_id']),
            visitor_id=int(data['visitor_id']),
            buddy_requirement=data['content'],
            request_time=datetime.now(),
            is_found=False
        )
        
        db.session.add(new_partner)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '搭子请求添加成功',
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in add_partner: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '添加搭子请求失败,请检查是否已发过请求'
        }), 500

# 编辑活动
@app.route('/editActivities', methods=['POST'])
def edit_activity():
    try:
        data = request.get_json()
        activity_id = data.get('activity_id')
        
        # 查找活动
        activity = Activity.query.get(activity_id)
        if not activity:
            return jsonify({
                'status': 'error',
                'message': '活动不存在'
            }), 404
            
        # 更新活动信息
        activity.name = data.get('name', activity.name)
        activity.type = data.get('type', activity.type)
        activity.start_time = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S') if data.get('start_time') else activity.start_time
        activity.end_time = datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M:%S') if data.get('end_time') else activity.end_time
        activity.description = data.get('description', activity.description)
        activity.flow = data.get('flow', activity.flow)
        
        # 如果提供了新的场地信息，更新场地关联
        if 'venue_id' in data:
            # 删除旧的关联
            ActivityInVenue.query.filter_by(activity_id=activity_id).delete()
            # 添加新的关联
            new_venue = ActivityInVenue(activity_id=activity_id, venue_id=data['venue_id'])
            db.session.add(new_venue)
            
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '活动更新成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in edit_activity: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': '更新活动失败'
        }), 500

# 删除活动
@app.route('/deleteActivities', methods=['POST'])
def delete_activity():
    data = request.get_json()
    activity_id = data.get('activity_id')
    activity = Activity.query.get(activity_id)
    organizer_activity = OrganizerManagesActivity.query.filter_by(activity_id=activity_id).first()
    if organizer_activity:
        db.session.delete(organizer_activity)
    activity_venue = ActivityInVenue.query.filter_by(activity_id=activity_id).first()
    if activity_venue:
        db.session.delete(activity_venue)

    db.session.delete(activity)
    db.session.commit()
    return jsonify({'status': 'success', 'message': '活动删除成功'})

print(app.url_map)  # 这会显示所有注册的路由

if __name__ == '__main__':
    app.run(debug=True)
