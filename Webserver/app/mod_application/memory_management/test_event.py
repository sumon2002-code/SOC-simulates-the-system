import unittest
import pickle

import event

class Testevents(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.old_event_manager = event.EventManager()
        cls.add_n = 5
        for _i in range(1, cls.add_n):
            title, des, t_s, t_e, group, r, url= \
                f'event_{_i}', f'event_{_i}' , 1702999710, 1703000710, \
                0, [], '#fff47'
            cls.old_event_manager.add_event(title, des, t_s, t_e, group, r, url)
        
        # Test for building the event pool with the method (__init__)
        cls.event_manager = event.EventManager(
            pickle_data=cls.old_event_manager.return_events_in_pickle)

    def test_list_events(self):
        self.assertEqual(
            type(self.event_manager.list_events), list)
        

    def test_delete_event(self):
        id = 2
        self.event_manager.delete_event(id)
        
        self.assertEqual(
            self.event_manager.events.get(id), None)
        
    def test_update_event(self):
        id = 1
        title = 'new title'
        start_time = 125487
        end_time = 115487
        description = 'new description'
        group_id = 1
        url = '#1254'
        reminders = [1564,100,60]
        self.event_manager.update_event(id,
                                        title=title, start_time=start_time,
                                        end_time=end_time, description=description,
                                        group_id=group_id, url=url, reminders=reminders)
        event = self.event_manager.events[id]
        self.assertEqual(event.id, id)
        self.assertEqual(event.title, title)
        self.assertEqual(event.start_time, start_time)
        self.assertEqual(event.end_time, end_time)
        self.assertEqual(event.description, description)
        self.assertEqual(event.group_id, group_id)
        self.assertEqual(event.url, url)
        self.assertEqual(event.reminders, reminders)
    
    def test_return_events_in_pickle(self):
        list_data = self.event_manager.list_events
        _temp_p = self.event_manager.return_events_in_pickle
        list_pikle = pickle.loads(_temp_p)
        self.assertEqual(len(list_data), len(list_pikle))

        
if __name__ == '__main__':
    unittest.main()
    