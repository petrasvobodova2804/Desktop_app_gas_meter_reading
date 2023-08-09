import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import zscore
from PIL import ImageTk, Image
from PIL import ImageDraw, ImageFont

def read_csv():
    # Open the CSV file
    with open('Orig_results.csv', 'r') as file:
        # Create a CSV reader
        reader = csv.reader(file)
        # Initialize lists to store the week numbers and gas meter values
        week_numbers = []
        gasmeter_values = []
        
            
        # Initialize a list to store the statistics for each reading
        gasmeter_values_list = []
        
        # Read each row in the CSV file
        for i, row in enumerate(reader):
            week_number = i + 1
            # Concatenate the values into a single string
            concatenated_value = ''.join(row)
            print(concatenated_value)
            gasmeter_values_list.append(concatenated_value)

            gasmeter_value = int(concatenated_value)
            week_numbers.append(week_number)
            gasmeter_values.append(gasmeter_value)

        # Convert the gas meter values to integers
        gasmeter_values = [int(value) for value in gasmeter_values_list]

        # Solves the reset to 0000 of gasmeter
        for i in range(0, len(gasmeter_values)-1):
            reset_index = None
            if (gasmeter_values[i] > gasmeter_values[i+1]):
                reset_index = i
                print("Gasmeter was reset")
                if reset_index is not None:
                    for j in range(reset_index+1, len(gasmeter_values)):
                        gasmeter_values[j] = gasmeter_values[j] + gasmeter_values[reset_index]

        # Compute differences between weekly values
        differences = []
        for i in range(0, len(gasmeter_values)-1):
            res_ = gasmeter_values[i+1] - gasmeter_values[i]
            differences.append(res_)


        # Calculate statistics
        mean = np.mean(differences)
        median = np.median(differences)
        minimum = np.min(differences)
        maximum = np.max(differences)
        standard_deviation = np.std(differences)
        diff = gasmeter_values[len(gasmeter_values)-1] - gasmeter_values[0]
        kwh = diff * 10.550
        kwh = round(kwh, 1)
        price = kwh * 0.275
        price = int(price)

        image_pil = Image.open("imgs/board.png").convert("RGB")
        # Resize the image if needed
        image_pil = image_pil.resize((600, 420))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype("arial.ttf", size=38)
        draw.text((300, 100), str(diff), fill=(245, 245, 245), font=font)
        font = ImageFont.truetype("arial.ttf", size=40)
        draw.text((420, 90), str(kwh), fill=(80, 80, 80), font=font)
        font = ImageFont.truetype("arial.ttf", size=35)
        draw.text((110, 290), str(minimum), fill=(80, 80, 80), font=font)
        draw.text((80, 330), str(maximum), fill=(80, 80, 80), font=font)
        font = ImageFont.truetype("arial.ttf", size=30)
        draw.text((238, 300), str(price), fill=(84, 169, 86), font=font)
        image_pil.save('imgs/output_board.png')


        # Plot the gas meter readings
        plt.plot(week_numbers, gasmeter_values)
        plt.xlabel('Week Number')
        plt.ylabel('Gas Meter Consumption [m3]')
        plt.title('Gas consumption overview')
        plt.grid(True)
        plt.savefig("imgs/gas_meter.png")
        plt.close()


        # Plot the gas meter readings
        # Styling
        plt.bar((week_numbers[:-1]), differences)
        plt.xlabel('Week Number')
        plt.ylabel('Gas Meter Consumption [m3]')
        plt.title('Gas consumption per week')
        plt.grid(True)
        plt.savefig("imgs/gas_meter_diff.png")
        plt.close()

        # Distribution of differencies
        # Create a box plot
        plt.boxplot(differences)
        # Add labels and title
        plt.xlabel('Differences')
        plt.ylabel('Change in Consumption')
        plt.title('Box Plot of Gas Consumption Differences')
        plt.grid(True)
        plt.savefig("imgs/box_plot_differences.png")
        plt.close()



        # Outliers (statisticke odchylky)
        z_scores = zscore(differences)
        threshold = 3  # Adjust the threshold as needed
        outliers = np.where(np.abs(z_scores) > threshold)[0]
        q1 = np.percentile(differences, 25)
        q3 = np.percentile(differences, 75)
        iqr = q3 - q1
        lower_bound = int(q1 - 1.5 * iqr)
        upper_bound = int(q3 + 1.5 * iqr)
        # Remove values outside the bounds
        differences = np.array(differences)
        filtered_differences = differences[(differences >= lower_bound) & (differences <= upper_bound)]
        

        # Create a histogram
        plt.hist(filtered_differences, bins=25, edgecolor='black')
        plt.xlabel('Differences')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.title('Distribution of Gas Consumption Differences')
        plt.savefig("imgs/distributions_of_differences.png")
        plt.close()

        # Create a KDE plot using Seaborn
        sns.kdeplot(filtered_differences, fill=True)
        plt.xlabel('Differences')
        plt.ylabel('Density')
        plt.title('Kernel Density Estimate of Gas Consumption Differences')
        plt.savefig("imgs/kernel_density.png")
        plt.close()

        # Create a k-means
        # Choose the number of clusters (k)
        from sklearn.cluster import KMeans
        k = 7  # Example number of clusters
        # Reshape the data to be a 2D array (one feature)
        X = differences.reshape(-1, 1)
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=k)
        labels = kmeans.fit_predict(X)
        plt.scatter(range(len(differences)), differences, c=labels, cmap='rainbow', marker='o')
        plt.xlabel('Index')
        plt.ylabel('Differences')
        plt.title('K-Means Clustering of Gas Consumption Differences')
        plt.grid()
        plt.savefig("imgs/clustering.png")
        plt.close()
        # Get the cluster centroids
        # Calculate cluster statistics
        cluster_stats = []
        for cluster_id in range(k):
            cluster_mask = labels == cluster_id
            cluster_data = differences[cluster_mask]
            
            cluster_mean = np.mean(cluster_data)
            cluster_median = np.median(cluster_data)
            cluster_std = np.std(cluster_data)
            cluster_range = np.max(cluster_data) - np.min(cluster_data)
            
            cluster_stats.append({
                'Cluster ID': cluster_id,
                'Mean': cluster_mean,
                'Median': cluster_median,
                'Std Deviation': cluster_std,
                'Range': cluster_range,
                'Size': np.sum(cluster_mask)
            })


        # Plot autocorrelation
        import pandas as pd
        from pandas.plotting import autocorrelation_plot
        df = pd.DataFrame({'Differences': differences})
        autocorrelation_plot(df['Differences'])
        plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('AutoCorrelation of Gas Consumption Differences')
        plt.savefig("imgs/autocorrelation.png")
        plt.close()

