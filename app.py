import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Marketing Campaign Analytics",
    page_icon="📊",
    layout="wide"
)


# Custom visual theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0B1020 0%, #151633 55%, #102A35 100%);
    color: #F8FAFC;
}

/* Hide the white Streamlit header and toolbar */
header[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

/* Remove excess top spacing */
.block-container {
    padding-top: 1.5rem !important;
}

/* Keep the main app background visible */
.stApp {
    background: linear-gradient(
        135deg,
        #0B1020 0%,
        #151633 55%,
        #102A35 100%
    );
}


/* Smooth hover effect for KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #20264A, #171B35);
    border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 14px;
    padding: 16px 18px;
    transition: transform 0.22s ease, box-shadow 0.22s ease,
                border-color 0.22s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #A78BFA;
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.28);
}

div[data-testid="stMetric}"] {
    cursor: default;
}


[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17152E 0%, #10252F 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.18);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #E0E7FF !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    color: #CBD5E1;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(139,92,246,0.24),
                                rgba(45,212,191,0.12));
    border: 1px solid rgba(167,139,250,0.35);
    padding: 20px 22px;
    border-radius: 18px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.18);
}

div[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 800;
}

div[data-testid="stSelectbox"] > label {
    color: #C4B5FD !important;
    font-weight: 600;
}

div[data-testid="stPlotlyChart"],
div[data-testid="stImage"] {
    border-radius: 16px;
}

hr {
    border-color: rgba(148,163,184,0.2);
}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_csv("bank-additional-full.csv", sep=";")

df = load_data()

st.title("📊 Marketing Campaign Conversion Dashboard")
st.caption("Future Interns | Data Science & Analytics | Task 3")
st.markdown(
    "Explore bank marketing campaign performance by contact method, "
    "campaign month, previous campaign outcome, and customer age."
)

st.sidebar.header("Dashboard Filters")

months = ["All"] + sorted(df["month"].unique().tolist())
selected_month = st.sidebar.selectbox("Campaign Month", months)

contacts = ["All"] + sorted(df["contact"].unique().tolist())
selected_contact = st.sidebar.selectbox("Contact Method", contacts)

filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["month"] == selected_month]

if selected_contact != "All":
    filtered_df = filtered_df[filtered_df["contact"] == selected_contact]

total_contacts = len(filtered_df)
conversions = (filtered_df["y"] == "yes").sum()
conversion_rate = (
    conversions / total_contacts * 100 if total_contacts > 0 else 0
)
non_conversions = total_contacts - conversions

st.subheader("Campaign Performance Overview")


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Contacts",
    f"{total_contacts:,}",
    help="Total number of campaign contacts after applying the selected filters."
)

col2.metric(
    "🎯 Conversions",
    f"{conversions:,}",
    help="Number of contacts where the customer successfully subscribed."
)

col3.metric(
    "📈 Conversion Rate",
    f"{conversion_rate:.2f}%",
    help="Successful conversions divided by total contacts, multiplied by 100."
)

col4.metric(
    "⏳ Non-Conversions",
    f"{non_conversions:,}",
    help="Number of contacts where the customer did not subscribe."
)


chart_df = filtered_df.copy()

chart_df["age_group"] = pd.cut(
    chart_df["age"],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=["18–25", "26–35", "36–45", "46–55", "56–65", "65+"]
)

def summarize(data, group_col):
    result = data.groupby(group_col, observed=False).agg(
        Contacts=("y", "count"),
        Conversions=("y", lambda x: (x == "yes").sum())
    )
    result["Conversion Rate (%)"] = (
        result["Conversions"] /
        result["Contacts"].replace(0, float("nan")) * 100
    ).fillna(0)
    return result

age_data = summarize(chart_df, "age_group")
contact_data = summarize(chart_df, "contact")
month_data = summarize(chart_df, "month")
previous_data = summarize(chart_df, "poutcome")

def style_chart(ax, title, xlabel, ylabel="Conversion Rate (%)"):
    ax.set_title(
    title,
    color="#F8FAFC",
    fontsize=11,
    fontweight="bold",
    pad=10
)
    ax.set_xlabel(xlabel, color="#CBD5E1")
    ax.set_ylabel(ylabel, color="#CBD5E1")
    ax.set_facecolor("#171B35")
    ax.tick_params(colors="#CBD5E1")
    ax.grid(axis="y", linestyle="--", alpha=0.22, color="#94A3B8")
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color("#475569")


def draw_bar_chart(data, title, xlabel, color="#8B5CF6"):
    plot_df = data.reset_index()
    category_col = plot_df.columns[0]

    # Prepare detailed hover information
    if "Contacts" in plot_df.columns and "Conversions" in plot_df.columns:
        plot_df["Non-Conversions"] = (
            plot_df["Contacts"] - plot_df["Conversions"]
        )

    fig = px.bar(
        plot_df,
        x=category_col,
        y="Conversion Rate (%)",
        title=title,
        color_discrete_sequence=[color],
        custom_data=[
            col for col in [
                "Contacts",
                "Conversions",
                "Non-Conversions"
            ] if col in plot_df.columns
        ]
    )

    hover_lines = [
        "<b>%{x}</b>",
        "Conversion Rate: %{y:.2f}%"
    ]

    for col in [
        "Contacts",
        "Conversions",
        "Non-Conversions"
    ]:
        if col in plot_df.columns:
            hover_lines.append(f"{col}: %{{customdata[{len(hover_lines)-2}]}}")

    fig.update_traces(
        hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
        marker_line_color="#C4B5FD",
        marker_line_width=1
    )

    fig.update_layout(
        title_font_color="#F8FAFC",
        title_font_size=14,
        title_x=0.02,
        paper_bgcolor="#171B35",
        plot_bgcolor="#171B35",
        font_color="#CBD5E1",
        xaxis_title=xlabel,
        yaxis_title="Conversion Rate (%)",
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(148,163,184,0.22)",
            zeroline=False
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        hoverlabel=dict(
            bgcolor="#252B4A",
            font_color="#FFFFFF",
            bordercolor="#8B5CF6"
        ),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


st.subheader("Conversion Rate by Age Group")
draw_bar_chart(
    age_data["Conversion Rate (%)"],
    "Conversion by Age",
    "Age Group",
    "#8B5CF6"
)

left, right = st.columns(2, gap="large")

with left:
    st.subheader("Conversion by Contact Method")
    draw_bar_chart(
        contact_data["Conversion Rate (%)"],
        "Contact Channel Performance",
        "Contact Method",
        "#2DD4BF"
    )

with right:
    st.subheader("Conversion by Previous Outcome")
    draw_bar_chart(
        previous_data["Conversion Rate (%)"].sort_values(
            ascending=False
        ),
        "Previous Campaign Performance",
        "Previous Outcome",
        "#A78BFA"
    )

st.subheader("Conversion Rate by Campaign Month")
draw_bar_chart(
    month_data["Conversion Rate (%)"].sort_values(ascending=False),
    "Monthly Conversion Performance",
    "Campaign Month",
    "#38BDF8"
)


st.subheader("🎯 Campaign Outcome Summary")

outcome_plot = previous_data.reset_index()
outcome_col = outcome_plot.columns[0]

outcome_plot["Non-Conversions"] = (
    outcome_plot["Contacts"] - outcome_plot["Conversions"]
)

fig = px.bar(
    outcome_plot,
    x=outcome_col,
    y="Conversion Rate (%)",
    color_discrete_sequence=["#8B5CF6"],
    custom_data=["Contacts", "Conversions", "Non-Conversions"]
)

fig.update_traces(
    hovertemplate=(
        "<b>Previous Campaign Outcome: %{x}</b><br>"
        "Conversion Rate: %{y:.2f}%<br>"
        "Total Contacts: %{customdata[0]:,}<br>"
        "Successful Conversions: %{customdata[1]:,}<br>"
        "Non-Conversions: %{customdata[2]:,}"
        "<extra></extra>"
    ),
    marker_line_color="#C4B5FD",
    marker_line_width=1
)

fig.update_layout(
    paper_bgcolor="#171B35",
    plot_bgcolor="#171B35",
    font_color="#CBD5E1",
    xaxis_title="Previous Campaign Outcome",
    yaxis_title="Conversion Rate (%)",
    hoverlabel=dict(
        bgcolor="#252B4A",
        font_color="#FFFFFF",
        bordercolor="#8B5CF6"
    ),
    yaxis=dict(gridcolor="rgba(148,163,184,0.22)"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("💡 Key Campaign Insights")

if total_contacts > 0:
    insight_df = filtered_df.copy()
    overall_conversion = (insight_df["y"] == "yes").mean() * 100

    contact_insights = insight_df.groupby("contact")["y"].apply(
        lambda x: (x == "yes").mean() * 100)

    month_insights = insight_df.groupby("month")["y"].apply(
        lambda x: (x == "yes").mean() * 100)

    previous_insights = insight_df.groupby("poutcome")["y"].apply(
        lambda x: (x == "yes").mean() * 100)

    age_insights = insight_df.copy()
    age_insights["age_group"] = pd.cut(
        age_insights["age"],
        bins=[0, 25, 35, 45, 55, 65, 100],
        labels=["18–25", "26–35", "36–45", "46–55", "56–65", "65+"]
    )

    age_rates = age_insights.groupby(
        "age_group", observed=False
    )["y"].apply(lambda x: (x == "yes").mean() * 100)

    best_contact = contact_insights.idxmax()
    best_month = month_insights.idxmax()
    worst_month = month_insights.idxmin()
    best_previous = previous_insights.idxmax()
    best_age = age_rates.idxmax()

    best_age_count = (
        age_insights["age_group"] == best_age
    ).sum()

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg,
                rgba(139,92,246,0.20),
                rgba(45,212,191,0.12));
            border: 1px solid rgba(167,139,250,0.4);
            border-radius: 18px;
            padding: 24px 28px;
            color: #F8FAFC;
            font-size: 17px;
            line-height: 1.8;
        ">
            <ul style="padding-left: 22px; margin: 0;">
                <li>
                    <b>Overall performance:</b>
                    The campaign converted
                    <b>{overall_conversion:.2f}%</b> of all contacts
                    ({(insight_df["y"] == "yes").sum():,} successful subscriptions).
                </li>
                <li>
                    <b>Contact channel:</b>
                    <b>{best_contact}</b> had the highest conversion
                    rate at <b>{contact_insights[best_contact]:.2f}%</b>.
                </li>
                <li>
                    <b>Campaign timing:</b>
                    <b>{best_month.title()}</b> had the highest monthly
                    conversion rate ({month_insights[best_month]:.2f}%),
                    while <b>{worst_month.title()}</b> had the lowest
                    ({month_insights[worst_month]:.2f}%).
                </li>
                <li>
                    <b>Previous campaign outcome:</b>
                    <b>{best_previous.title()}</b> had the highest
                    conversion rate at
                    <b>{previous_insights[best_previous]:.2f}%</b>.
                </li>
                <li>
                    <b>Age group:</b>
                    The <b>{best_age}</b> group had the highest
                    conversion rate at <b>{age_rates[best_age]:.2f}%</b>
                    ({best_age_count:,} contacts).
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    st.caption(
        "Note: These insights describe associations in the dataset, "
        "not proven causes. Monthly and age-group rates should be "
        "interpreted alongside their contact volumes."
    )
else:
    st.info("No contacts match the selected filters.")


