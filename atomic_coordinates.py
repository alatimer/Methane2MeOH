import pickle

catlistobj = pickle.load(open('dftobj.pkl','rb'))
catlistobj = catlistobj.filter(lambda x: x.ets_ch4!=None)
