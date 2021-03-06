from sklearn.cluster import KMeans
import sklearn
import numpy as np
import pickle
import matplotlib.pyplot as plt
import folium
import pandas as pd
from branca.colormap import linear


heat_map_image = pickle.load(open("dump/heat_map_image{}".format("[(59900,30120)-(59830,30220)]"), "rb"))

r1 = np.ones((10000, 1))
for type_ in heat_map_image.keys():
    if type_ != "json":
        r1 = np.hstack((r1, np.reshape(heat_map_image[type_], (10000, 1))))


kmeans = KMeans(n_clusters=4, random_state=0).fit(r1)
plt.imshow(np.reshape(kmeans.labels_, (100, 100)))
plt.savefig("images/model")
heat_map_image["model"] = np.reshape(kmeans.labels_, (100, 100))

for type_ in heat_map_image.keys():
    if type_ != "json":
        t = np.transpose(heat_map_image[type_])
        data = pd.DataFrame(np.reshape(t, (10000,)), columns=["values1"])
        data['id'] = [i for i in range(10000)]
        # create map
        colormap = linear.YlGn.scale(
            data.values1.min(),
            data.values1.max())
        print(data.values1.min(), data.values1.max())

        problems_dict = data.set_index('id')['values1']

        m = folium.Map(location=[59, 30], zoom_start=4)

        folium.GeoJson(
            heat_map_image["json"],
            name='values1',
            style_function=lambda feature1: {
                'fillColor': colormap(problems_dict[feature1['id']]),
                'color': 'black',
                'weight': 1,
                'dashArray': '5, 5',
                'fillOpacity': 0.5,
                'opacity': 0.5
            }
        ).add_to(m)

        folium.LayerControl().add_to(m)

        m.save('result/{}.html'.format(type_))

