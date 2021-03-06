# Copyright 2016-2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta, datetime

from odoo.tests import common


class TestHrTimesheetTaskStage(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.project = self.env['project.project'].create(
            {'name': 'Test project'})
        self.analytic_account = self.project.analytic_account_id
        self.task = self.env['project.task'].create({
            'name': 'Test task',
            'project_id': self.project.id,
        })
        task_type_obj = self.env['project.task.type']
        self.stage_open = task_type_obj.create({
            'name': 'New',
            'closed': False,
            'project_ids': [(6, 0, self.project.ids)],
        })
        self.stage_close = task_type_obj.create({
            'name': 'Done',
            'closed': True,
            'project_ids': [(6, 0, self.project.ids)],
        })
        self.line = self.env['account.analytic.line'].create({
            'date_time': datetime.now() - timedelta(hours=1),
            'task_id': self.task.id,
            'account_id': self.analytic_account.id,
            'name': 'Test line',
        })

    def test_open_close_task(self):
        self.line.action_close_task()
        self.assertEqual(self.line.task_id.stage_id, self.stage_close)
        self.line.action_open_task()
        self.assertEqual(self.line.task_id.stage_id, self.stage_open)

    def test_toggle_task_stage(self):
        self.line.action_toggle_task_stage()
        self.assertTrue(self.line.task_id.stage_id.closed)
        self.assertTrue(self.line.is_task_closed)
        self.line.action_toggle_task_stage()
        self.assertFalse(self.line.task_id.stage_id.closed)
        self.assertFalse(self.line.is_task_closed)
