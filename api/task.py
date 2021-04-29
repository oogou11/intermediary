"""
定时任务相关
"""
import datetime
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .service import AuditService


jobstores = {
    'redis': RedisJobStore(**settings.REDIS),
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)


class CoreTasks(object):
    """
    异步定时任务
    """
    def create_core_job(self, project):
        """
        固定时间, 项目结束日期后会自动进行匹配选标
        :param project: 项目信息
        :return:
        """
        self._excute_select_company(project)
        self._excute_is_abolished_project(project)

    def _excute_select_company(self, project):
        """
        系统自动选表
        :param project:
        :return:
        """
        excute_time = project.finish_time
        id = 'selected_{}'.format(project.id)
        scheduler.add_job(AuditService.finish_biding_project, 'date', id=id, jobstore='redis',
                          run_date=excute_time, args=[project.id])

    def _excute_is_abolished_project(self, project):
        """
        执行时间：项目结束后日期+2天
        判断是否否作废项目：项目状态不是选标，则作废项目。
        :param project:
        :return:
        """
        one_day = datetime.timedelta(days=2)
        excute_time = project.finish_time + one_day
        id = 'abolish_{}'.format(project.id)
        scheduler.add_job(AuditService.finish_biding_project, 'date', id=id, jobstore='redis',
                          run_date=excute_time, args=[project.id])

# 启动定时任务程序
scheduler.start()
