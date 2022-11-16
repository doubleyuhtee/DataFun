import pandas as pd
import plotly.express as px

import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"
if __name__ == '__main__':
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        qbs_df = pd.read_csv("resource/qbs.csv")
        team_abbrv_map = pd.read_csv("resource/teamabbrvmap.csv")
        super_bowl_winners = pd.read_csv("resource/superbowls.csv")
        super_bowl_losers = pd.read_csv("resource/superbowls.csv")

        qbs_df['Player'] = qbs_df['Player'].apply(lambda x: str(x).split("+")[0].split("(")[0].strip())
        fig = px.scatter(qbs_df, x="Year", y="Y/G", color="Player")
        fig.update_yaxes(range=[240, 350])

        super_bowl_winners["Tm"] = super_bowl_winners["Tm"].apply(lambda x: str(x).split(":")[1].split("(")[0].strip())
        super_bowl_winners = pd.merge(super_bowl_winners, team_abbrv_map, left_on="Tm", right_on="Name", how='left')
        winning_yards = pd.merge(super_bowl_winners, qbs_df, left_on=["Year", "ABR"], right_on=["Year", "Tm"])

        super_bowl_losers["Tm"] = super_bowl_losers["Tm"].apply(lambda x: str(x).split("defeated")[1].split("(")[0].strip())
        super_bowl_losers = pd.merge(super_bowl_losers, team_abbrv_map, left_on="Tm", right_on="Name", how='left')
        losing_yards = pd.merge(super_bowl_losers, qbs_df, left_on=["Year", "ABR"], right_on=["Year", "Tm"])

        fig.add_trace(go.Scatter(x=winning_yards["Year"], y=winning_yards["Y/G"], name="SuperbOwl Winner"))
        fig.add_trace(go.Scatter(x=losing_yards["Year"], y=losing_yards["Y/G"], name="Superbowl Loser"))

        fig.write_html("TopPassers.html")
