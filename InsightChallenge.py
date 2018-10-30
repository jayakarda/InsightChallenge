
# coding: utf-8

# In[256]:


from itertools import islice
import sys
import os

def main():

    # This method reads a file and stores them into a list.
    def create_data_structure(fname):
        if not os.path.isfile(fname):
            print("File path {} doesn't exist.".format(fname))
            sys.exit()
        with open (fname , 'r') as f:
            lines = islice(f, 600000)
            table = [line.split(';') for line in lines]
            total_applications = len(table)
        return (table, total_applications)



    # This method takes in 2 arguments namely processed_document and total_applications which is returned from create_data_structure.
    # It returns states_counter object where the keys are the state names and the values are number of certified applications.
    # It also returns top 10 states for certified applications.
    # This method uses get_top_n_elements to get states_counter and top_states


    def top_10_states(processed_document, total_applications):
        state_row_index = get_index(processed_document, ["LCA_CASE_EMPLOYER_STATE", "WORKSITE_STATE"])
        status_row_index =  get_index(processed_document, ["STATUS", "CASE_STATUS"])

        state_data= []
        status_data= []
        for row in processed_document:
            state_data.append(row[state_row_index])
            status_data.append(row[status_row_index])
        states_counter, top_states = get_top_n_elements(processed_document,state_data,status_data, 10)
        return (states_counter, top_states)


    # Similarly as the above method, this method takes in 2 arguments namely processed_document and total_applications which is returned from create_data_structure.
    # It returns occupations_counter object where the keys are the occupation names and the values are number of certified applications.
    # It also returns top 10 occupations for certified applications.
    # This method uses get_top_n_elements to get occupations_counter and top_occupations

    def top_10_occupations(processed_document, total_applications):
        socname_row_index = get_index(processed_document, ["LCA_CASE_SOC_NAME", "SOC_NAME"])
        status_row_index =  get_index(processed_document, ["STATUS", "CASE_STATUS"])

        socname_data= []
        status_data= []
        for row in processed_document:
            socname_data.append(row[socname_row_index])
            status_data.append(row[status_row_index])
        occupations_counter, top_occupations= get_top_n_elements(processed_document, socname_data,status_data, 10)
        return (occupations_counter, top_occupations)

    #This methods get the index value for a column name.

    def get_index(processed_document, column_names =[]):
        first_row = processed_document[0]
        for column_name in column_names:
            if column_name in first_row:
                column_index = first_row.index(column_name)
                return column_index
            else:
                pass


    # This method zips 2 lists, creates a dictionary of items in first list and gets top_n_elements from the resulting
    # dictionary. This is a utility method.
    def get_top_n_elements(processed_document, data_list1, data_list2, num): 
        data_counter  = {}
        for x,y in zip(data_list1, data_list2):
            value = 0
            if y == 'CERTIFIED':
                dict_value = data_counter.get(x, 0)
                data_counter[x] = dict_value + 1
        return (data_counter, sorted(data_counter, key=data_counter.get, reverse=True)[:num])

    # This is another utility method which writes to a file the desired output.
    def write_to_file(top_list, top_counter, total_applications, fname):
        with open (fname, 'w+') as f:
            for element in top_list:
                perc_val = "{0:.00%}".format(float(top_counter.get(element))/total_applications)
                f.write(element)
                f.write(';')
                f.write(str(top_counter.get(element)))
                f.write(';')
                f.write(str(perc_val)+ "\n")
    
    filename = sys.argv[1]
    #filename = '/Users/jayakarda/Desktop/InsightProject/H1B_FY_2016.csv'
    processed_document, total_applications = create_data_structure(filename)
    states_counter, top_state_list = top_10_states(processed_document, total_applications)
    occupations_counter, top_occupation_list = top_10_occupations(processed_document, total_applications)
    directory = 'output'
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    cwd = os.getcwd()
    occup_file = cwd + "/"+ directory+ "/top_10_occupations.txt"
    print occup_file
    state_file = cwd + "/"+ directory+ "/top_10_states.txt"
    print state_file
    write_to_file(top_occupation_list, occupations_counter, total_applications, occup_file)
    write_to_file(top_state_list, states_counter, total_applications, state_file)
    

if __name__== "__main__":
    main()


# In[241]:





# In[ ]:



    

