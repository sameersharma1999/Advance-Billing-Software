from App.backend_database.billingdb import FetchData


class InterBilling:

    def getvar(self):
        pass
        # print(c.iti)

    # def print_list(self, li):
    #     print(li)

    @staticmethod
    def id_search(id_search):
        return_list = FetchData.fetchdata(id_search)
        return return_list
    @staticmethod
    def mobile_search(mobile):
        return_lst=FetchData.fetchCustomerdet(mobile)
        #print(return_lst)
        return return_lst

    @staticmethod
    def mobile_search_full(mobile):
        return_lst = FetchData.fetchAllCustomerdet(mobile)
        # print(return_lst)
        return return_lst
