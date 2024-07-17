import unittest
import pickle

import task

class TestTasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.old_tasks = task.TasksManager()
        cls.add_n = 5
        for _i in range(1, cls.add_n):
            name, t_s= f'task_{_i}', 1702999710
            cls.old_tasks.add_task(name, t_s)
        
        # Test for building the task pool with the method (__init__)
        cls.tasks = task.TasksManager(
            pickle_data=cls.old_tasks.return_tasks_in_pickle)

    def test_list_tasks(self):
        self.assertEqual(
            type(self.tasks.list_tasks), list)
        

    def test_delete_task(self):
        id = 2
        self.tasks.delete_task(id)
        
        self.assertEqual(
            self.tasks.tasks.get(id), None)
        
    def test_done_task(self):
        id = 1
        done_task = self.tasks.tasks[id].done
        self.tasks.done_task(id)

        self.assertNotEqual(done_task,
                            self.tasks.tasks[id].done)

    def test_update_task(self):
        id = 1
        name, t_s, group_title = 'update', 1, 'Pos'
        self.tasks.update_task(id, name, t_s, group_title=group_title)
        task = self.tasks.tasks[id]
        self.assertEqual(task.id, id)
        self.assertEqual(task.name, name)
        self.assertEqual(task.time_start, t_s)
        self.assertEqual(task.group_title, group_title)
    
    def test_return_tasks_in_pickle(self):
        list_data = self.tasks.list_tasks
        _temp_p = self.tasks.return_tasks_in_pickle
        list_pikle = pickle.loads(_temp_p)
        self.assertEqual(len(list_data), len(list_pikle))

        
if __name__ == '__main__':
    unittest.main()
    