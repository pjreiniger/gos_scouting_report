from functools import partial
from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# read in data
df = pd.read_csv("C:/Users/sienn/Downloads/frc_good_mock_data.csv")

# add new columns
df["Coral Total Teleop"] = df["Coral L1 Teleop"] + df["Coral L2 Teleop"] + df["Coral L3 Teleop"] + df["Coral L4 Teleop"]
df["Coral Total Auto"] = df["Coral L1 Auto"] + df["Coral L2 Auto"] + df["Coral L3 Auto"] + df["Coral L4 Auto"]

df["Coral Total Points Teleop"] = df["Coral L1 Teleop"]*2 + df["Coral L2 Teleop"]*3 + df["Coral L3 Teleop"]*4 + df["Coral L4 Teleop"]*5
df["Algae Total Points Teleop"] = df["Algae in Net Teleop"]*4 + df["Algae in Processor Teleop"]*6
df["Total Teleop Points"] = df["Coral Total Points Teleop"] + df["Algae Total Points Teleop"]

df["Coral Total Points Auto"] = df["Coral L1 Auto"]*3 + df["Coral L2 Auto"]*4 + df["Coral L3 Auto"]*6 + df["Coral L4 Auto"]*7
df["Algae Total Points Auto"] = df["Algae in Net Auto"]*4 + df["Algae in Processor Auto"]*6
df["Total Auto Points"] = df["Coral Total Points Auto"] + df["Algae Total Points Auto"]

df["Algae in Net and Processor Teleop"] = df["Algae in Net Teleop"] + df["Algae in Processor Teleop"]
df["Algae in Net and Processor Auto"] = df["Algae in Net Auto"] + df["Algae in Processor Auto"]
position = df["End Position"]
df["Endgame Points"] = np.where(position == "Park", 2, np.where(position == "Shallow", 6, np.where(position == "Deep", 12, 0)))


df["Total Points Scored"] = df["Total Teleop Points"] + df["Total Auto Points"] + df["Endgame Points"]

# upcoming alliance lineup
red_teams = [5743, 5750, 1783]
blue_teams = [2955, 9895, 8219]
all_teams = red_teams + blue_teams

# filter df by team number
new_df = df.loc[df["Team Number"].isin(all_teams)]

# averages df
averages_by_team = new_df.groupby("Team Number").mean(numeric_only=True).reset_index()
print(averages_by_team)
print(new_df)

# endgame df
endgame_df = new_df.groupby('Team Number')['End Position'].value_counts().unstack(fill_value=0).reset_index()
print(endgame_df)

# color map
color_map = {str(team): "#FF5733" for team in red_teams}  # Red teams
color_map.update({str(team): "#1F77B4" for team in blue_teams})  # Blue teams
ticktext = [f'<span style="color:{color_map[team]};">{team}</span>' for team in ]


# Define the UI
app_ui = ui.page_navbar(
    ui.nav_panel(
        "General Data",
        ui.card(
            ui.output_ui("teleop_auto_points_scatter")
        ),
        ui.card(
            ui.output_ui("total_points_boxplot")
        )
    ),
    ui.nav_panel(
        "Auto Data",
        ui.card(
            ui.output_ui("coral_algae_auto_scatter")
        ),
        ui.card(
            ui.output_ui("coral_level_distribution_auto_bar")
        ),
        ui.card(
            ui.output_ui("coral_point_distribution_auto_bar")
        )        
    ),
    ui.nav_panel(
        "Teleop Data",
        ui.card(
            ui.output_ui("coral_algae_teleop_scatter")
        ),
        ui.card(
            ui.output_ui("net_processor_teleop")
        ),
         ui.card(
            ui.output_ui("coral_level_distribution_teleop_bar")
        ),
                 ui.card(
            ui.output_ui("coral_point_distribution_teleop_bar")
        )
    ),
    ui.nav_panel(
        "Endgame Data",
        ui.card(
            ui.output_ui("endgame_bar")
        )
    ),
    ui.nav_panel(
        "Alliance Selection",
        ui.card(
            ui.output_data_frame("key_stats_dt")
        )
    ),
    title="GoS REEFSCAPE Data Science Report",
)

# Define the server logic
def server(input, output, session):
    @output
    @render.ui
    def total_points_boxplot():
        fig = px.box(new_df, 
                    x="Team Number Str", 
                    y="Total Points Scored", 
                    color="Team Number Str",
                    category_orders={"Team Number Str": new_df["Team Number Str"].tolist()},  # Ensure x-axis is ordered
                    color_discrete_map=color_map
                    )

        # Step 6: Update x-axis labels if needed
        fig.update_layout(
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=new_df["Team Number Str"].tolist(),
                ticktext=new_df["Team Number Str"].tolist(),
                tickfont=dict(size=14)
            )
        )
    
        return ui.HTML(fig.to_html(full_html=False))

    @output
    @render.ui
    def coral_algae_teleop_scatter():

        def color_picker(team_num, red_teams):
            if team_num in red_teams:
                return "red"
            else:
                return "blue"

        x = averages_by_team["Coral Total Teleop"]
        y = averages_by_team["Algae in Net and Processor Teleop"]
        teams = averages_by_team["Team Number"]

        fig = px.scatter(x=x, y=y, text=teams, labels={'x': "Avg Coral Scored", 'y': "Avg Algae Scored in Net"},
                        title="Coral vs Algae TELEOP")

        colors = [color_picker(team, red_teams) for team in teams]
        fig.update_traces(marker=dict(color=colors,
                                    symbol='circle', size=10),
                        textposition="middle left")

        return ui.HTML(fig.to_html(full_html=False))
    
    @output
    @render.ui
    def teleop_auto_points_scatter():
        x = averages_by_team["Total Teleop Points"]
        y = averages_by_team["Total Auto Points"]

        # Create the plot
        fig = px.scatter(x=x, y=y, text=teams, labels={'x': "Total Teleop Points", 'y': "Total Auto Points"},
                        title="Teleop vs Auto Points")

        # Add custom color for each point based on the team number
        colors = [color_picker(team, red_teams) for team in teams]  # Apply color_picker correctly
        fig.update_traces(marker=dict(color=colors,
                                    symbol='circle', size=10),
                        textposition="middle left")
        
        return ui.HTML(fig.to_html(full_html=False))
    
    @output
    @render.ui
    def net_processor_teleop():
        # Step 3: Define x-axis values
        x = averages_by_team["Team Number"]
        y1 = averages_by_team["Algae in Net Teleop"]
        y2 = averages_by_team["Algae in Processor Teleop"]

        # Step 4: Define colors for x-axis labels
        color_map = {str(team): "#FF5733" for team in red_teams}  # Red teams
        color_map.update({str(team): "#1F77B4" for team in blue_teams})  # Blue teams

        # Generate colored tick labels
        ticktext = [f'<span style="color:{color_map[team]};">{team}</span>' for team in x]

        # Step 5: Create the bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name="Net",
            marker=dict(color="#83DCDD", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name="Processor",
            marker=dict(color="#FFB480", line=dict(color="white", width=1))
        ))

        # Step 6: Update layout with grouped colored x-axis labels
        fig.update_layout(
            barmode="stack",
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=all_teams,
                ticktext=ticktext,  # Apply colored labels
                tickfont=dict(size=14)  # Adjust font size if needed
            ),
            yaxis_title="Avg Algae in Net / Processor",
            title="Algae in Processor and Net TELEOP",
            legend_title="Algae Type",
            template="plotly_white"
        )


        return ui.HTML(fig.to_html(full_html=False)) 

    @output
    @render.ui
    def coral_algae_auto_scatter():
        x = averages_by_team["Coral Total Auto"]
        y = averages_by_team["Algae in Net and Processor Auto"]
        teams = averages_by_team["Team Number"]

        fig = px.scatter(x=x, y=y, text=teams, labels={'x': "Avg Coral Scored", 'y': "Avg Algae Scored in Net"}, title="Coral vs Algae AUTO")

        colors = [color_picker(team, red_teams) for team in teams]  # Apply color_picker correctly
        fig.update_traces(marker=dict(color=colors, symbol='circle', size=10), textposition="middle left") 
        return ui.HTML(fig.to_html(full_html=False)) 

    @output
    @render.ui
    def coral_level_distribution_teleop_bar():
        x = averages_by_team["Team Number"]
        y1 = averages_by_team["Coral L1 Teleop"]
        y2 = averages_by_team["Coral L2 Teleop"]
        y3 = averages_by_team["Coral L3 Teleop"]
        y4 = averages_by_team["Coral L4 Teleop"]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name="Coral L1",
            marker=dict(color="#9BE3DF", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name="Coral L2",
            marker=dict(color="#F7898A", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y3,
            name="Coral L3",
            marker=dict(color="#FACE9F", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y4,
            name="Coral L4",
            marker=dict(color="#FFE493", line=dict(color="white", width=1))
        ))

        fig.update_layout(
            barmode="stack",  # Stack the bars
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=all_teams,
                ticktext= ticktext,
                tickfont=dict(size=14)  # Adjust font size if needed
            ),
            yaxis_title="Avg Coral in L1, L2, L3, L4",
            title="Coral Level Distribution Teleop",
            legend_title="Coral Levels",
            template="plotly_white"
        )

        return ui.HTML(fig.to_html(full_html=False)) 
    @output
    @render.ui
    def coral_level_distribution_auto_bar():
        averages_by_team["Team Number"] = averages_by_team["Team Number"].astype(str)
        x = averages_by_team["Team Number"]
        y1 = averages_by_team["Coral L1 Teleop"]
        y2 = averages_by_team["Coral L2 Teleop"]
        y3 = averages_by_team["Coral L3 Teleop"]
        y4 = averages_by_team["Coral L4 Teleop"]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name="Coral L1",
            marker=dict(color="#9BE3DF", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name="Coral L2",
            marker=dict(color="#F7898A", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y3,
            name="Coral L3",
            marker=dict(color="#FACE9F", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y4,
            name="Coral L4",
            marker=dict(color="#FFE493", line=dict(color="white", width=1))
        ))

        fig.update_layout(
            barmode="stack",  # Stack the bars
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=all_teams,
                ticktext= ticktext,
                tickfont=dict(size=14)  # Adjust font size if needed
            ),
            yaxis_title="Avg Coral in L1, L2, L3, L4",
            title="Coral Level Distribution Teleop",
            legend_title="Coral Levels",
            template="plotly_white"
        )

        return ui.HTML(fig.to_html(full_html=False)) 

    @output
    @render.ui
    def coral_point_distribution_teleop_bar():
        # coral level distribution -- stacked bar graph
        averages_by_team["Team Number"] = averages_by_team["Team Number"].astype(str)
        x = averages_by_team["Team Number"]
        y1 = averages_by_team["Coral L1 Teleop"]*2
        y2 = averages_by_team["Coral L2 Teleop"]*3
        y3 = averages_by_team["Coral L3 Teleop"]*4
        y4 = averages_by_team["Coral L4 Teleop"]*5

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name="Coral L1",
            marker=dict(color="#9BE3DF", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name="Coral L2",
            marker=dict(color="#F7898A", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y3,
            name="Coral L3",
            marker=dict(color="#FACE9F", line=dict(color="white", width=1))
        ))

        fig.add_trace(go.Bar(
            x=x,
            y=y4,
            name="Coral L4",
            marker=dict(color="#FFE493", line=dict(color="white", width=1))
        ))

        fig.update_layout(
            barmode="stack",  # Stack the bars
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=all_teams,
                ticktext= ticktext,
                tickfont=dict(size=14)  # Adjust font size if needed
            ),
            yaxis_title="Avg Coral in L1, L2, L3, L4",
            title="Coral Point Distribution by Level Teleop",
            legend_title="Coral Levels",
            template="plotly_white"
        )
        return ui.HTML(fig.to_html(full_html=False)) 
    @output
    @render.ui
    def endgame_bar():
        # Convert "Team Number" to string if not already done
        endgame_df["Team Number"] = endgame_df["Team Number"].astype(str)
        x = endgame_df["Team Number"]
        y1 = endgame_df["Park"]
        y2 = endgame_df["Shallow"]
        y3 = endgame_df["Deep"]

        # Create the bar graph
        fig = go.Figure()

        # Add the first bar (Park)
        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name="Park",
            marker=dict(color="#EB89B5", line=dict(color="white", width=1))
        ))



        # Add the second bar (Shallow), stacked on top of Park
        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name="Shallow",
            marker=dict(color="#FFD7E9", line=dict(color="white", width=1))
        ))

        # Add the third bar (Deep), stacked on top of Park + Shallow
        fig.add_trace(go.Bar(
            x=x,
            y=y3,
            name="Deep",
            marker=dict(color="#FFF2AF", line=dict(color="white", width=1))
        ))

        # Update layout for stacking and aesthetics
        fig.update_layout(
            barmode="stack",  # Stack the bars
            xaxis=dict(
                title="Team",
                tickmode="array",
                tickvals=all_teams,
                ticktext= ticktext,
                tickfont=dict(size=14)  # Adjust font size if needed
            ),
            yaxis_title="Endgame Status",
            title="Endgame Status",
            legend_title="Status Levels",
            template="plotly_white"
        )
        return ui.HTML(fig.to_html(full_html=False)) 
    
    @output
    @render.data_frame
    def key_stats_dt():
        return averages_by_team  
    

app = App(app_ui, server)
