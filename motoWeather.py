# MOTO WEATHER CONFIGURATION: set up your list of lat/lon points below, lists of times of the day you care about, and your openweathermap.org api key
locations=[[38.029649, -78.807175],[38.044573, -78.725776]]
times=[8,9,16,17,18] # 8am, 9am, 4pm, 5pm, 6pm
key="123456789abcdefghijklmnop"
maximums={"rain":1,"temp":25}	# whatever keys are available here: https://openweathermap.org/api/one-call-api#parameter , we'll take the boolean
minimums={"temp":7}	# intersection of these max/min (ie, "if too much rain, we don't ride, or too low temps, we don't ride")	

# DO NOT EDIT ANYTHING BELOW THIS POINT!
import requests,json,os,time,datetime,numpy
def getWeather(lat,lon):
	jsondata={}
	if os.path.exists("motoWeather.json"):			# previous queries would be saved to motoWeather.json
		with open("motoWeather.json") as json_file:
			jsondata = json.load(json_file)
		if str(lat)+","+str(lon) in jsondata.keys():	# requirement 1: a query was made previously for this location
			lasttime=jsondata[str(lat)+","+str(lon)]["timestamp"]
			if lasttime>time.time()-60*60:		# requirement 2: a query was made within the last hour
				print("use-saved:",lat,lon)
				return jsondata
	# either motoWeather.json was not found, or this location has not been queried, or the query is considered "expired", then requery
	print("requery:",lat,lon)
	query="https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(lon)+"&units=metric&appid="+key
	response = requests.get(query) #https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0
	data={ str(lat)+","+str(lon) : {"timestamp":time.time(),"data":response.json()} } # query returns a dict, we package it a level deeper
	jsondata={**jsondata,**data}				# merge the two dicts, where "data" overwrites like-entries (try it yourself: a={"A":1,"B":2}; b={"C":3,"A":4}; z={**a,**b} # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-take-union-of-dictionari
	with open("motoWeather.json", 'w') as outfile: #https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
		json.dump(jsondata, outfile)
	return jsondata

def main():
	# step 1, query weather forcast for all locations (or read in saved forecast from file, if fresh)
	for lat,lon in locations:
		data=getWeather(lat,lon) # getWeather() will be returning ALL locations each time. a word on structure: data["lat,lon"] has keys 'timestamp','data'. data sub-dict has keys 'lat','lon','timezone','timezone_offset','current','minutely','hourly','daily'. 'hourly' is a list of dicts. each hourly dict has a whole variety of keys: most notably: 'dt','temp','humidity','clouds','visibility','wind_speed','wind_deg','wind_gust','pop','rain']
	# step 2, process data, checking each location and hour.
	passes=numpy.zeros((len(locations),len(times))) # what do we need to ride? any hour where all weather conditions are met, at all locations. so we'll check all locations and all hours, and log passes or fails here. then look for rows which are all passes
	for l,(lat,lon) in enumerate(locations):
		print(l,lat,lon)
		hours=data[str(lat)+","+str(lon)]["data"]["hourly"] ; h=-1 # h is just a counter, serving the role of an index for passes
		for hour in hours:
			dt=hour["dt"]				# seconds since the epoch, eg 1652994000
			if dt>time.time()+24*60*60:		# if timestamp is more than 24 hours away from "now", skip it?
				continue
			dt=datetime.datetime.fromtimestamp(dt)	# as a datetime object, eg datetime.datetime(2022, 5, 19, 17, 0)
			ho=dt.strftime('%H')			# get the hour from the datetime object, eg 17 --> 5PM
			if int(ho) not in times:
				continue
			weride=True ; h+=1
			#print(h)
			for key in maximums.keys():
				if key in hour.keys():
					if maximums[key] < hour[key]:
						print("poor conditions:",ho,lat,lon,key,">",maximums[key],"(",hour[key],")")
						weride=False
			for key in minimums.keys():
				if key in hour.keys():
					if minimums[key] > hour[key]:
						print("poor conditions:",ho,lat,lon,key,"<",minimums[key],"(",hour[key],")")
						weride=False
			if weride:
				passes[l,h]=1
				#print("WE RIDE!")
				#conditions= [ k+":"+str(hour.get(k,0)) for k in maximums.keys() ]
				#conditions+=[ k+":"+str(hour.get(k,0)) for k in minimums.keys() ]
				#print("(",",".join(conditions)+")")
					
			#else:
			#	print("(we don't ride)")
			#print(h,hour)
	print( "\t"+"\t".join([str(t) for t in times]) )
	for i in range(len(locations)):
		s=[ "l"+str(i) ] + [ str(p) for p in passes[i,:] ]
		print( "\t".join(s) )


main()		