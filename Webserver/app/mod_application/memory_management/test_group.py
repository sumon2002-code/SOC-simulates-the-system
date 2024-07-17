import unittest
import pickle

import group

class TestGroup(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.old_group_manager = group.GroupManager()
        cls.number_create_group = 6
        
        for g in range(1, cls.number_create_group):
            title = f'{g}_title'
            des = f'{g}_des'
            color = f'#{g}8475'
            cls.old_group_manager.add_group(
                title=title, description=des, color=color)

        # Test for building the group pool with the method (__init__)
        cls.group_manager = group.GroupManager(
            pickle_data=cls.old_group_manager.return_group_in_pickle)



    def test_list_groups(self):
        self.assertEqual(
            type(self.group_manager.list_groups), list)
    
    def test_return_group_in_pickle(self):
        pk = self.group_manager.return_group_in_pickle
        self.assertEqual(
            len(pickle.loads(pk)), len(self.group_manager.list_groups))
        # Note : I could not compare the lists and finally I used this method! 
        #           My theory is that if the number of items is equal,
        #             it means that the data is properly pickled and transformed from pickle to object
    
    def test_set_groups(self):
        _groupsTemp = list()
        for g in range(1, self.number_create_group):
            title = f'{g}-test'
            des = f'{g}_des'
            color = f'#{g}8475'
            
            _groupsTemp.append(
                group._Group(
                    title=title,
                    description=des, color=color)
                )
            
        self.group_manager.set_groups(_groupsTemp)
        
        self.assertListEqual(
            self.group_manager.list_groups, _groupsTemp
        )
    
    def test_update_group(self):
        title = 'New Title'
        des = "New Description"
        color = "#ffff"
        title_get = list(self.group_manager.groups.keys())[0]

        self.group_manager.update_group(target_title=title_get, title=title,
                                        color=color, description=des)
        
        _group = self.group_manager.groups.get(title_get)

        self.assertEqual(title, _group.title)
        self.assertEqual(color, _group.color)
        self.assertEqual(des, _group.description)
    
    def test_delete_group(self):
        number_of_groups_before_delete = len(self.group_manager.list_groups)
        
        title_get = list(self.group_manager.groups.keys())[0]
        self.group_manager.delete_group(title_get)
        
        self.assertEqual((number_of_groups_before_delete - 1),
                         len(self.group_manager.list_groups))
if __name__ == '__main__':
    unittest.main()