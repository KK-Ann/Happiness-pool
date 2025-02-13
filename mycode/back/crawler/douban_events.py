import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from model import db, Activity,OrganizerManagesActivity
from app import app

def parse_time(time_str):
    """解析时间字符串"""
    # 处理类似 "01月09日 周四 21:45-23:59" 的格式
    try:
        # 提取日期和时间
        date_match = re.search(r'(\d{2})月(\d{2})日', time_str)
        time_match = re.search(r'(\d{2}:\d{2})', time_str)
        
        if date_match and time_match:
            month, day = date_match.groups()
            time = time_match.group(1)
            current_year = datetime.now().year
            
            # 组合日期时间
            datetime_str = f"{current_year}-{month}-{day} {time}:00"
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"时间解析错误: {e}")
    return None

def crawl_douban_events():
    for i in range(0, 10):
        url = f'https://shanghai.douban.com/events/week-all?start={i*10}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
        try:
            with app.app_context():
                response = requests.get(url, headers=headers)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 找到所有活动项
                events = soup.find_all('div',class_="info")

                for event in events:
                    #print(event)
                    try:
                        # 提取活动信息
                        title = event.find('span', itemprop='summary').text.strip()
                        print(title)
                        time_str = event.find('li', class_='event-time').text.strip()
                        print(time_str)
                        fee_str = event.find('strong').text.strip()
                        print(fee_str)
                        channel = event.find('a', target="db-event-owner" ).text.strip()
                        # 解析时间
                        start_time = parse_time(time_str)
                        if not start_time:
                            continue
                            

                        
                        # 创建活动记录
                        activity = Activity(
                            name=title,
                            type='文化类',  # 可以根据实际分类优化
                            start_time=start_time,
                            end_time=start_time,  # 可以根据实际结束时间优化
                            registration_channel=channel,
                            description=f"费用: {fee_str}",
                            flow=100  # 默认人流量
                        )

                        
                        # 检查活动是否已存在
                        existing_activity = Activity.query.filter_by(
                            name=title,
                            start_time=start_time
                        ).first()
                        
                        if not existing_activity:
                            db.session.add(activity)
                            db.session.flush()

                        activityOrganizer = OrganizerManagesActivity(
                            activity_id=activity.activity_id,
                            organizer_id=3,
                        )
                        # 检查活动是否已存在
                        existing_oa = OrganizerManagesActivity.query.filter_by(
                            activity_id=activity.activity_id,
                            organizer_id=3,
                        ).first()

                        if not existing_activity:
                            db.session.add(activityOrganizer)
                            #db.session.flush()
                        
                        db.session.commit()
                        print(f"成功添加活动: {title}")
                        
                    except Exception as e:
                        print(f"处理活动时出错: {e}")
                        db.session.rollback()
                        continue
                
                print("爬虫任务完成")
                
        except Exception as e:
            print(f"爬虫运行错误: {e}")

if __name__ == "__main__":
    crawl_douban_events() 