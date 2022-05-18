# motoWeather
a quick script to check if we should commute to work by bike

Enter the lattitude and longitude of points along your route

```Line 2: locations=[[38.029649, -78.807175],[38.044573, -78.725776]]```

Enter your commute times (eg, I'm flexible, and willing to commute to work anywhere between 8-10am (i'd enter 8,9), and come home anywhere between 4 and 7 (16,17,18)

```Line 3: times=[8,9,16,17,18] # 8am, 9am, 4pm, 5pm, 6pm```

make an openweathermap.org account (free subscription should do!), and enter your api key

```Line 4: key="123456789abcdefghijkl"```


consider what conditions you're willing to commute in: skip it when it's too cold? add "temp" to "minimums". okay with a light drizzle, but want to avoid the downpour? add "rain.1h" to "maximums" (see here for a full list of parameters: https://openweathermap.org/api/one-call-api#parameter )

```
Line 5: maximums={"rain.1h":1,"temp":25}
Line 6: minimums={"temp":7}	
```

run the code. (eg: python3 motoWeather.py). 

we'll query openweathermap (and save off the results, so as to limit excessive queries if you were to re-run within the next hour) for the hourly forecast for the points along your route. 

then we'll compare the results against the constraints you imposed ("quite cold early in the morning, but maybe later it's fine!"), and present you with a chart of the results:

eg:
```
0 [myhouse] [myhouse]
poor conditions: 16 [myhouse] [myhouse] temp > 25 ( 26.23 )
poor conditions: 17 [myhouse] [myhouse] temp > 25 ( 25.79 )
1 38.029649 -78.807175
poor conditions: 16 38.029649 -78.807175 temp > 25 ( 25.9 )
poor conditions: 17 38.029649 -78.807175 temp > 25 ( 25.6 )
2 38.044573 -78.725776
poor conditions: 16 38.044573 -78.725776 temp > 25 ( 26.21 )
poor conditions: 17 38.044573 -78.725776 temp > 25 ( 26.33 )
poor conditions: 18 38.044573 -78.725776 temp > 25 ( 25.1 )
3 [mywork] [mywork]
poor conditions: 16 [mywork] [mywork] temp > 25 ( 26.3 )
poor conditions: 17 [mywork] [mywork] temp > 25 ( 26.48 )
	8	9	16	17	18
l0	1.0	1.0	0.0	0.0	1.0
l1	1.0	1.0	0.0	0.0	1.0
l2	1.0	1.0	0.0	0.0	0.0
l3	1.0	1.0	0.0	0.0	1.0
```
where we're looking for two (one morning, one evening) columns of 1s (all weather conditions passed, at this time, at each location). in this example, our overly conservative limitation of a max temp of 25C (for Virginia, that is!) says there are no evening times to ride home! 
