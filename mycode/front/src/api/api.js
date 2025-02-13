import { postAction, getAction } from "./config";

// 注册
export const visitorRegister = (param) => postAction("/visitor/register", param)
export const organizerRegister = (param) => postAction("/organizer/register", param)
export const managerRegister = (param) => postAction("/manager/register", param)

// 登录
export const visitorLogin = (param) => postAction("/visitor/login", param)
export const organizerLogin = (param) => postAction("/organizer/login", param)
export const managerLogin = (param) => postAction("/manager/login", param)

// 获取场所信息
export const getVenues = () => getAction("/venues")
// 获取场所详情
export const getVenueDetail = (param) => postAction("/venuesDetail",param)
// 获取活动信息
export const getActivities = () => getAction("/activities")
// 获取活动详情和评论，搭子信息
export const getActivityDetail = (param) => postAction("/activitiesDetail",param)

// 发布评论（post 评论 活动id 用户id 时间）
export const addComment = (param) => postAction("/addComments",param)
// 发布搭子（post 搭子 活动id 用户id 时间）
export const addPartner = (param) => postAction("/addPartners",param)
// visitor获取搭子信息 （post  visitor_id）
export const getPartners = (param) => postAction("/visitor_buddy",param)

// visitor更改搭子状态（post 搭子id 状态）
export const changePartnerStatus = (param) => postAction("/changeBuddyStatus",param)
// visitor删除搭子（post 搭子id 用户id）
export const deletePartner = (param) => postAction("/deleteBuddy",param)

//manager获取organizer信息
export const getOrganizers = () => getAction("/organizers")
// manger更改organizer状态（post 组织者id 状态）
export const changeOrganizerStatus = (param) => postAction("/changeOrganizerStatus",param)
// organizer获取活动信息
export const getOrganizerActivities = (param) => postAction("/organizer_activities",param)
// organizer删除活动
export const deleteActivity = (param) => postAction("/deleteActivities",param)
//organizer增加活动
export const addActivity = (param) => postAction("/addActivities",param)
// organizer编辑活动
export const editActivity = (param) => postAction("/editActivities",param)