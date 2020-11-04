# -*- coding: utf-8 -*-
import scrapy


class TopicfollowerItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # userID---唯一标识
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 回答数
    answer_count = scrapy.Field()
    # 文章数
    articles_count = scrapy.Field()
    # 粉丝数
    follower_count = scrapy.Field()
    # 性别
    gender = scrapy.Field()


class UserfollowerItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # 这个用户是从谁的粉丝列表爬取的
    whose_follower = scrapy.Field()
    # userID---唯一标识
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 回答数
    answer_count = scrapy.Field()
    # 文章数
    articles_count = scrapy.Field()
    # 粉丝数
    follower_count = scrapy.Field()
    # 性别
    gender = scrapy.Field()


class UserfollowingItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # 这个用户是从谁的关注者列表爬取的
    followed_by_who = scrapy.Field()
    # userID---唯一标识
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 回答数
    answer_count = scrapy.Field()
    # 文章数
    articles_count = scrapy.Field()
    # 粉丝数
    follower_count = scrapy.Field()
    # 性别
    gender = scrapy.Field()


class UserquestionItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # 问题标题
    title = scrapy.Field()
    # 问题id--唯一标识
    question_id = scrapy.Field()
    # 问题描述
    detail = scrapy.Field()
    # 提问者id
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 该问题的回答数
    answer_count = scrapy.Field()
    # 问题链接
    url = scrapy.Field()
    # 问题的关注者数
    follower_count = scrapy.Field()
    # 问题创建时间戳
    created = scrapy.Field()
    # 问题修改时间
    updated_time = scrapy.Field()
    # 所属话题
    topics = scrapy.Field()


class UseranswerItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # ----------answer-----------
    # 回答id--唯一标识
    answer_id = scrapy.Field()
    # 回答内容
    content = scrapy.Field()
    # 赞同数
    voteup_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 是否允许转载
    is_copyable = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()

    # -----------question--------
    # 问题id
    question_id = scrapy.Field()
    # 问题标题
    title = scrapy.Field()
    # 问题描述
    detail = scrapy.Field()
    # 该问题的回答数
    answer_count = scrapy.Field()
    # 问题的关注者数
    follower_count = scrapy.Field()
    question_created_time = scrapy.Field()
    question_updated_time = scrapy.Field()
    # 所属话题
    topics = scrapy.Field()

    # ------------author----------
    # 回答者id
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 性别
    gender = scrapy.Field()


class QuestionanswerItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # ----------answer-----------
    # 回答id--唯一标识
    answer_id = scrapy.Field()
    # 回答内容
    content = scrapy.Field()
    # 赞同数
    voteup_count = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 是否允许转载
    is_copyable = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()

    # -----------question--------
    # 问题id
    question_id = scrapy.Field()
    # 问题标题
    title = scrapy.Field()
    # 问题描述
    detail = scrapy.Field()
    question_created_time = scrapy.Field()
    question_updated_time = scrapy.Field()
    # 所属话题
    topics = scrapy.Field()

    # ------------author----------
    # 回答者id
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 性别
    gender = scrapy.Field()


class UserinformationItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # userID---唯一标识
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 回答数
    answer_count = scrapy.Field()
    # 提问数
    question_count = scrapy.Field()
    # 商业问题数
    commercial_question_count = scrapy.Field()
    # 文章数
    articles_count = scrapy.Field()
    # 专栏数
    columns_count = scrapy.Field()
    # 粉丝数
    follower_count = scrapy.Field()
    # 关注者数
    following_count = scrapy.Field()
    # 收藏数
    favorite_count = scrapy.Field()
    # 被收藏数
    favorited_count = scrapy.Field()
    # 想法数
    pins_count = scrapy.Field()
    # 公共编辑数
    logs_count = scrapy.Field()
    # 获得赞数
    voteup_count = scrapy.Field()
    # 获得感谢数
    thanked_count = scrapy.Field()
    # 开设live数
    hosted_live_count = scrapy.Field()
    # 参与live数
    participated_live_count = scrapy.Field()
    # 关注专栏数
    following_columns_count = scrapy.Field()
    # 关注话题数
    following_topic_count = scrapy.Field()
    # 关注问题数
    following_question_count = scrapy.Field()
    # 关注收藏夹数
    following_favlists_count = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 是否活跃
    is_active = scrapy.Field()
    # 是否广告商
    is_advertiser = scrapy.Field()
    # 是否允许私信
    allow_message = scrapy.Field()
    # 领域
    business = scrapy.Field()
    # 位置
    location = scrapy.Field()
    # 职业
    job = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 学校
    school = scrapy.Field()
    # 专业
    major = scrapy.Field()


class TopicdiscussionItem(scrapy.Item):
    belongs_to = scrapy.Field()
    # ----------answer-----------
    # 回答id--唯一标识
    answer_id = scrapy.Field()
    # 回答内容
    content = scrapy.Field()
    # 赞同数
    voteup_count = scrapy.Field()
    # 评论数 ok
    comment_count = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()

    # -----------question--------
    # 问题id
    question_id = scrapy.Field()
    # 问题标题
    title = scrapy.Field()

    # ------------author----------
    # 回答者id
    url_token = scrapy.Field()
    # 昵称
    name = scrapy.Field()
