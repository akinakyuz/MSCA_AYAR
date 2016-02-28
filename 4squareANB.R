library(RJSONIO)
library(RCurl)
library(leaflet)

options(RCurlOptions = list(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")))

# First, read in file with latitudes and longitudes of major cities
# Obtained from http://notebook.gaslampmedia.com/download-zip-code-latitude-longitude-city-state-county-csv/
ll = read.csv('zips.csv',sep=",",head=TRUE)

str(ll)
ll <- subset(ll, state == "IL")
head(ll)


clientid = "QDGQJ3FQY2ESOGDGDMW0V2JWJDTT5ARHAF4L54J0FK2GXJGR"
clientsecret = "XXYD2MGL5YPW5KCUA5N40RNKLEDAERANU4U2NLJUUWNP1YN3"




venue_name = c()
venue_lat = c()
venue_long = c()
venue_city = c()
venue_state = c()
venue_country = c()
venue_checkins = c()
venue_users = c()

dim(ll)
# &query=chicago&v=20130815
for (i in 1:dim(ll)[1]) {
  lat = ll$latitude[i]
  long = ll$longitude[i]
   # Do query and parse results
  query = paste("https://api.foursquare.com/v2/venues/explore?client_id=",clientid,"&client_secret=",clientsecret,"&ll=",lat,",",long,'&query=chicago&v=20160215',sep="")
  result = getURL(query)
  data <- fromJSON(result)
  
  # For each result, save a bunch of fields, you can tweak this to your liking
  if (length(data$response$groups[[1]]$items) > 0) {
    for (r in 1:length(data$response$groups[[1]]$items)) {
      tmp = data$response$groups[[1]]$items[[r]]$venue
      venue_name = c(venue_name,tmp$name)
      venue_lat = c(venue_lat,tmp$location$lat)
      venue_long = c(venue_long,tmp$location$lng)
      venue_city = c(venue_city,tmp$location$city)
      venue_state = c(venue_state,tmp$location$state)
      venue_country = c(venue_country,tmp$location$country)
      venue_checkins = c(venue_checkins,tmp$stats[1])
      venue_users = c(venue_users,tmp$stats[2])
    }
  }
}

# SAVE RESULT
save(venue_name,venue_lat,venue_long,venue_city,venue_state,venue_country,venue_checkins,venue_users,file='venuesResult.RData')
#venue_name
# create data frame
data1 = as.data.frame(cbind(venue_checkins,venue_name,venue_lat,venue_long,venue_checkins,venue_users))
str(data)
# any duplicate results?
dsub = subset(data,!duplicated(data))
names(dsub) = c("latlong","checkins","latitude","longitude","name")

# Export to file so we can use in Google Fusion Table
tabley = dsub[,2:5]
#tabley
write.table(tabley,file="import.csv",quote=TRUE,sep=",",row.names=FALSE)

df <- read.csv('import.csv', header = TRUE)
m <- leaflet(df) %>% addProviderTiles("CartoDB.Positron") %>% addCircleMarkers()
m
