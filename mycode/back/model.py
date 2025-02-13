from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
db = SQLAlchemy()

class Visitor(db.Model):
    __tablename__ = 'visitor'
    visitor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    favorite_activity_type = db.Column(db.Enum('文化类', '体育类', '娱乐类'), nullable=False)

    @staticmethod
    def init_db():
        test_data = [
            Visitor(name="Alice", password="password1", email="alice@example.com", favorite_activity_type="文化类"),
            Visitor(name="Bob", password="password2", email="bob@example.com", favorite_activity_type="体育类")
        ]
        db.session.add_all(test_data)
        db.session.commit()


class Organizer(db.Model):
    __tablename__ = 'organizer'
    organizer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    compliance_status = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def init_db():
        test_data = [
            Organizer(name="David", password="password3", email="david@example.com", compliance_status=True),
            Organizer(name="Eve", password="password4", email="eve@example.com", compliance_status=False)
        ]
        db.session.add_all(test_data)
        db.session.commit()


class Manager(db.Model):
    __tablename__ = 'manager'
    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)

    @staticmethod
    def init_db():
        test_data = [
            Manager(name="Frank", password="password5", email="frank@example.com"),
            Manager(name="Grace", password="password6", email="grace@example.com")
        ]
        db.session.add_all(test_data)
        db.session.commit()


class Activity(db.Model):
    __tablename__ = 'activity'
    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum('文化类', '体育类', '娱乐类'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    flow = db.Column(db.Integer, nullable=True)
    registration_channel = db.Column(db.String(100), nullable=True)
    registration_start_time = db.Column(db.DateTime, nullable=True)
    registration_end_time = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def init_db():
        test_data = [
            Activity(
                name="【上剧场】《暗恋桃花源》专属版", start_time=datetime(2025, 2, 28, 19, 30), end_time=datetime(2025, 3, 16, 16, 30),
                type="文化类", description="一个文化活动", flow=100, registration_channel="官网",
                registration_start_time=datetime(2025, 2, 28, 19, 30), registration_end_time=datetime(2024, 11, 3, 17, 0)
            ),
            Activity(
                name="音乐剧《SIX》上海站", start_time=datetime(2025, 5, 21, 19, 30),
                end_time=datetime(2025, 5, 21, 19, 30),
                type="文化类", description="“野心、智慧、大爱、财富、美貌、独立”这些形容词一一代表了16世纪英国君主亨利八世的六位伟大的皇后。在成为亨利八世的妻子之后,这六位伟大女性的姓名曾淹没在历史的洪流,被视为国王的附庸和脚注。如今,她们跳出了条条框框,唱出了自己的心声,做回真正的自己,为自己正名。",
                flow=100, registration_channel="官网",

            ),
            Activity(
                name="体育赛事", start_time=datetime(2024, 11, 10, 15, 0), end_time=datetime(2024, 11, 10, 20, 0),
                type="体育类", description="一场精彩的体育赛事", flow=200, registration_channel="App",
                registration_start_time=datetime(2024, 11, 2, 10, 0), registration_end_time=datetime(2024, 11, 5, 18, 0)
            )
        ]
        db.session.add_all(test_data)
        db.session.commit()


class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    latitude = db.Column(db.Numeric(10, 7), nullable=False)

    @staticmethod
    def init_db():
        test_data = []
        filtered_data = pd.read_csv('filtered_venue.csv')
        for _, row in filtered_data.iterrows():
            venue = Venue(
                name=row['名称'],
                description=row['小分类'],
                city=row['真实城市'],
                county=row['区域'],
                street=row['地址'],
                phone=row['电话'],
                longitude=row['经度'],
                latitude=row['纬度']
            )
            test_data.append(venue)

        db.session.add_all(test_data)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comment'
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.visitor_id'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), primary_key=True)
    comment_content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def init_db():
        test_data = [
            Comment(visitor_id=1, activity_id=1, comment_content="很好的活动", rating=5),
            Comment(visitor_id=2, activity_id=2, comment_content="非常棒的体验", rating=4)
        ]
        db.session.add_all(test_data)
        db.session.commit()


class VisitorRequestBuddy(db.Model):
    __tablename__ = 'visitor_request_buddy'
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.visitor_id'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), primary_key=True)
    buddy_requirement = db.Column(db.Text, nullable=True)
    request_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_found = db.Column(db.Boolean, nullable=True, default=False)

    @staticmethod
    def init_db():
        test_data = [
            VisitorRequestBuddy(visitor_id=1, activity_id=1, buddy_requirement="寻找一起参加活动的伙伴"),
            VisitorRequestBuddy(visitor_id=2, activity_id=2, buddy_requirement="需要开车接送", is_found=True)
        ]
        db.session.add_all(test_data)
        db.session.commit()


class OrganizerManagesActivity(db.Model):
    __tablename__ = 'organizer_manages_activity'
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.organizer_id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), primary_key=True)
    latest_operation = db.Column(db.Enum('增添活动', '更改介绍', '更改报名信息', '更改时间'), nullable=True)
    latest_operation_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    @staticmethod
    def init_db():
        test_data = [
            OrganizerManagesActivity(organizer_id=1, activity_id=1, latest_operation="增添活动"),
            OrganizerManagesActivity(organizer_id=2, activity_id=2, latest_operation="更改时间")
        ]
        db.session.add_all(test_data)
        db.session.commit()


class ManagerManagesOrganizer(db.Model):
    __tablename__ = 'manager_manages_organizer'
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.organizer_id'), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=False)

    @staticmethod
    def init_db():
        test_data = [
            ManagerManagesOrganizer(organizer_id=1, manager_id=1),
            ManagerManagesOrganizer(organizer_id=2, manager_id=2)
        ]
        db.session.add_all(test_data)
        db.session.commit()


class ActivityInVenue(db.Model):
    __tablename__ = 'activity_in_venue'
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)

    @staticmethod
    def init_db():
        test_data = [
            ActivityInVenue(activity_id=1, venue_id=1),
            ActivityInVenue(activity_id=2, venue_id=1)
        ]
        db.session.add_all(test_data)
        db.session.commit()

# 定义Data类，包含所有表类


# 初始化所有表的测试数据
def init_all_data():
    Visitor.init_db()
    Organizer.init_db()
    Manager.init_db()
    Activity.init_db()
    Venue.init_db()
    Comment.init_db()
    VisitorRequestBuddy.init_db()
    OrganizerManagesActivity.init_db()
    ManagerManagesOrganizer.init_db()
    ActivityInVenue.init_db()