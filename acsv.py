import csv

######################################## Functions definition
def csvwrite_acc_loss(filename):
	with open(filename, mode='w') as csvfile:
		fieldnames = ['Accuracy', 'Losses']
		csvwriter = csv.writer(csvfile, delimiter='\t')

		csvwriter.writerow(fieldnames)
		data_length = int(len(history.history['acc']))
		for i in range(data_length):
			csvwriter.writerow([history.history['acc'][i], history.history['loss'][i]])

######################################## Functions definition