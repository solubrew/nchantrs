


class tableWindow(QWidget):
	def __init__(self):
		QWidget.__init__(self)
	def createFrameModel(self):
		''
		path = '/home/solubrew/DataWorkRepo/EquitiesSETs/Securities.sqlite'
		table = 'pyf_ibHistTrack'
		self.model = DataFrameModel()
		data = next(sonql.doc(path).read({'views': [table]}))
		self.df = DataFrame(data.dikt[table]['records'], columns=data.dikt[table]['columns'])
		window = 30
		col = 'Close'
		self.df = self.df.sort_values(by=['Date'], ascending=True)
		self.df['Close'] = self.df['Close'].apply(float)
		self.df['Low'] = self.df['Low'].apply(float)
		self.df['High'] = self.df['High'].apply(float)
		self.df['median'] = self.df[col].rolling(window).median()
		self.df['stddev'] = self.df[col].rolling(window).std()
		self.df['+1SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)
		self.df['+2SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)*2
		self.df['+3SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)*3
		self.df['+4SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)*4
		self.df['+5SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)*5
		self.df['+6SIG'] = self.df[col].apply(float)+self.df['stddev'].apply(float)*6
		self.df['-1SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)
		self.df['-2SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)*2
		self.df['-3SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)*3
		self.df['-4SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)*4
		self.df['-5SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)*5
		self.df['-6SIG'] = self.df[col].apply(float)-self.df['stddev'].apply(float)*6
		day30Mean = self.df[col].rolling(30).mean()
		day30STD = self.df[col].rolling(30).std()
		self.df['upperBB'] = day30Mean + 2*day30STD
		self.df['lowerBB'] = day30Mean - 2*day30STD
		self.df = self.df.sort_values(by=['Date'], ascending=False)
		window = 7
		self.df = rsi(self.df, window)
		self.model.setDataFrame(self.df)
		return self
