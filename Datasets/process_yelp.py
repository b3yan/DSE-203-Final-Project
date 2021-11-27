import json, csv, os.path


def correct_path(inpath):
	abspath = os.path.join(os.path.dirname(__file__))
	return os.path.join(abspath, inpath)


def json_iterator(filepath):
	try:
		file = open(filepath, 'r', encoding="utf8")
	except IOError as e:
		print("I/O error({0}): {1}".format(e.errno, e.strerror))
	for line in file:
		line = json.loads(line)
		yield line


def write_csv(filepath, data=None, header=None, append=False):

	mode = 'a'
	if append == False:
		mode = 'w'
		try:
			os.remove(filepath)
		except OSError as e:
			pass

	try:
		outputfile = open(filepath, mode, encoding="utf8")
	except IOError as e:
		print("I/O error({0}): {1}".format(e.errno, e.strerror))

	# print("Destination: ", filepath)
	output = csv.writer(outputfile, quoting=csv.QUOTE_NONNUMERIC)
	if header is not None:
		output.writerow(header)
	if data is None:
		return

	for row in data:
		output.writerow(row)

	outputfile.close()


def extract_cols(filepath, outpath=None, cols=[], chunk_size=10000):
	if(outpath is None):
		outpath = filepath[:-5] + '.csv'

	# Write header
	write_csv(outpath, header=cols)

	# Reading json
	data = json_iterator(filepath)

	i = 0
	data_chunk = []
	for row in data:
		if (i<chunk_size):
			i = i + 1
			data_chunk.append([v.strip() if type(v) == str
			else v for k, v in row.items() if k in cols])
		else:
			data_chunk.append([v.strip() if type(v) == str
			else v for k, v in row.items() if k in cols])
			write_csv(filepath=outpath, data=data_chunk, append=True)
			data_chunk=[]
			i = 0

	# Write residual data
	if i != 0:
		write_csv(filepath=outpath, data=data_chunk, append=True)



def process_yelp_business(filepath, outpath=None, chunk_size=10000):

 	filepath = correct_path(filepath)
 	extract_cols(filepath,cols=['business_id','name','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','attributes','categories','hours'] , chunk_size=chunk_size)

	# if outpath is None:
	#  	outpath = filepath[:-5]
	#
	#  citypath = os.path.join(outpath + '_city.csv')
	#  categorypath = os.path.join(outpath + '_categories.csv')
	#  # Reading json
	#  data = json_iterator(filepath)
	#
	#  # Collect values
	#  categories = set([])
	#  cities = set([])
	#  for business in data:
	#  	city = (business['city'], business['state'])
	#  	cities.add(city)
	#
	#  	business_id = business['business_id']
	#  	raw = business['categories']
	#  	if raw is None:
	#  	    continue
	#  	raw = [x.strip() for x in raw.split(",")]
	#  	for category in raw:
	#  		categories.add((business_id, category))
	#
	#  write_csv(citypath, cities, header=['city', 'state'])
	#  write_csv(categorypath, categories, header=['business_id','category'])


def process_yelp_user(filepath, outpath=None, chunk_size = 10000):
 	filepath = correct_path(filepath)
 	extract_cols(filepath, cols=['user_id','name',
 			'review_count','yelping_since', 'useful', 'funny', 'cool','fans',
 			'average_stars', 'compliment_hot','compliment_more',
 			'compliment_profile','compliment_cute','compliment_list',
 			'compliment_note','compliment_plain','compliment_cool',
 			'compliment_funny','compliment_writer','compliment_photos'],
 			chunk_size=chunk_size)

	 # if outpath is None:
	 # 	outpath = filepath[:-5] + '_friendship.csv'
	 #
	 # # Reading json
	 # data = json_iterator(filepath)
	 #
	 # # Write header
	 # write_csv(outpath, header=['user1', 'user2'])
	 # # Collect values
	 # friendships_chunk = []
	 # i = 0
	 # for user in data:
	 # 	friendlist = user['friends']
	 # 	if friendlist == "None":
	 # 		continue
	 # 	friendlist = [x.strip() for x in friendlist.split(",")]
	 # 	for friend in friendlist:
	 # 		if(friend is None):
	 # 			continue
	 # 		# Add only one of the two pairs that would be found
	 # 		if (user['user_id'] < friend):
	 # 			if (i < chunk_size):
	 # 				i += 1
	 # 				friendships_chunk.append((user['user_id'], friend))
	 # 			else:
	 # 				friendships_chunk.append((user['user_id'], friend))
	 # 				write_csv(outpath, data=friendships_chunk, append=True)
	 # 				friendships_chunk = []
	 # 				i = 0
	 # if i != 0:
	 # 	write_csv(outpath, data=friendships_chunk, append=True)


def process_yelp_review(filepath, outpath=None, chunk_size=10000):
 	filepath = correct_path(filepath)
 	extract_cols(filepath, cols=['review_id',
 			'user_id', 'business_id','stars', 'useful', 'funny', 'cool', 'text', 'date'],
 			chunk_size=chunk_size)

def process_yelp_photos(filepath, outpath=None, chunk_size=10000):
	filepath = correct_path(filepath)
	extract_cols(filepath, cols=['photo_id', 'business_id', 'caption', 'label'],
				 chunk_size=chunk_size)

def process_yelp_tip(filepath, outpath=None, chunk_size=10000):
	filepath = correct_path(filepath)
	extract_cols(filepath, cols=['user_id', 'business_id', 'text', 'date', 'compliment_count'],
				 chunk_size=chunk_size)

process_yelp_business('../yelp_academic_dataset_business.json')
print('Processed business json')

process_yelp_user('../yelp_academic_dataset_user.json')
print('Processed user json')

process_yelp_review('../yelp_academic_dataset_review.json')
print('Processed review json')

process_yelp_photos('../yelp_academic_dataset_photos.json')
print('Processed photos json')

process_yelp_tip('../yelp_academic_dataset_tip.json')
print('Processed tip json')