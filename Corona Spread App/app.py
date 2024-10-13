from flask import Flask, render_template
import pandas as pd
import folium

pairs = []
maps = []


# To get top countries
def find_top_confirmed_country(corona_df, n=15):
    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    top_country = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return top_country


country_corona_df = pd.read_csv("dataset1.csv")
top_country = find_top_confirmed_country(country_corona_df)
country_pairs = [(country, confirmed) for country, confirmed in zip(
    top_country.index, top_country['Confirmed'])]
pairs.append(country_pairs)

country_corona_df = country_corona_df[['Lat', 'Long_', 'Confirmed']]
country_corona_df = country_corona_df.dropna()

country_map = folium.Map(location=[34.223334, -82.461707],
                         tiles='Stamen toner',
                         zoom_start=8)


def circle_maker(x):
    folium.Circle(location=[x[0], x[1]],
                  radius=float(x[2]),
                  color="red",
                  popup='confirmed cases:{}'.format(x[2])).add_to(country_map)


country_corona_df.apply(lambda x: circle_maker(x), axis=1)

country_html_map = country_map._repr_html_()
maps.append(country_html_map)


# To get top states datas
def find_top_confirmed_states(corona_df, n=15):
    by_country = corona_df.groupby('Province_State').sum()[
        ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    top_states = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return top_states


def circle_maker(x):
    folium.Circle(location=[x[0], x[1]],
                  radius=float(x[2]),
                  color="red",
                  popup='confirmed cases:{}'.format(x[2])).add_to(states_map)


corona_state_df = pd.read_csv("dataset2.csv")
top_states = find_top_confirmed_states(corona_state_df)
state_pairs = [(province_state, confirmed)
               for province_state, confirmed in zip(top_states.index, top_states['Confirmed'])]
pairs.append(state_pairs)
corona_state_df = corona_state_df[['Lat', 'Long_', 'Confirmed']]
corona_state_df = corona_state_df.dropna()

states_map = folium.Map(location=(
    22.50607289476002, 80.20934295937263), tiles='Stamen toner', zoom_start=8)


corona_state_df.apply(lambda x: circle_maker(x), axis=1)

states_html_map = states_map._repr_html_()
maps.append(states_html_map)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", cmap=maps, pairs=pairs)


if __name__ == "__main__":
    app.run(debug=True)
