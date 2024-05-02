class visual(object):
    def scatter(self, df1): 
        df = df1.copy().dropna(axis=0, subset = ['bedrooms', "tax paid","sold price"])
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
    
        ax.scatter(df['bedrooms'],df['tax paid'], df['sold price']) 

        ax.set_title('The Sold Price vs Bedrooms vs Tax Paid')
        ax.set_xlabel('Bedrooms')
        ax.set_ylabel('Tax Paid')
        ax.set_zlabel('Sold Price') 

        plt.show()

    def histogram(self, df1): 
        df = df1.copy().dropna(axis=0, subset = ['sold price'])
        plt.hist([df['sold price']],150,align='mid')

        # Add a title
        plt.title('Histogram of Sold Price')

        # Add x and y labels
        plt.xlabel('Sold Price')
        plt.ylabel('Frequency')

        # Show the plot!
        plt.show()

