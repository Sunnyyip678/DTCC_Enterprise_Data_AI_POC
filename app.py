import pandas as pd
import streamlit as st

# 1. 页面基本配置
st.set_page_config(
    page_title="Enterprise Data & AI Capability POC", layout="wide"
)
st.title("🛡️ Enterprise Data Governance, Quality & AI Platform")
st.caption("Integrated Data Product for Regulatory Risk Management")


# 2. 内存中动态生成模拟测试数据
@st.cache_data
def load_data():
    cp = pd.DataFrame(
        [
            {
                "counterparty_id": "CP001",
                "legal_name": "Apex Capital LLC",
                "credit_rating": "AAA",
                "entity_type": "Bank",
                "country": "US",
            },
            {
                "counterparty_id": "CP002",
                "legal_name": "Beacon Trust Corp",
                "credit_rating": "AA",
                "entity_type": "Fund",
                "country": "UK",
            },
            {
                "counterparty_id": "CP003",
                "legal_name": "Crestline Partners",
                "credit_rating": None,
                "entity_type": "Corporate",
                "country": "US",
            },
            {
                "counterparty_id": "CP004",
                "legal_name": "Delta Global Ltd",
                "credit_rating": "BBB",
                "entity_type": "Bank",
                "country": "DE",
            },
            {
                "counterparty_id": "CP005",
                "legal_name": "Echo Financial Group",
                "credit_rating": "A",
                "entity_type": "Fund",
                "country": "JP",
            },
            {
                "counterparty_id": "CP005",
                "legal_name": "Echo Financial Group",
                "credit_rating": "A",
                "entity_type": "Fund",
                "country": "JP",
            },  # 故意重复
        ]
    )

    exp = pd.DataFrame(
        [
            {
                "exposure_id": "E001",
                "counterparty_id": "CP001",
                "gross_exposure_usd": 12500000,
                "net_exposure_usd": 10000000,
                "as_of_date": "2026-09-17",
            },
            {
                "exposure_id": "E002",
                "counterparty_id": "CP002",
                "gross_exposure_usd": 8300000,
                "net_exposure_usd": 7000000,
                "as_of_date": "2026-09-17",
            },
            {
                "exposure_id": "E003",
                "counterparty_id": "CP003",
                "gross_exposure_usd": -500000,
                "net_exposure_usd": 400000,
                "as_of_date": "2026-09-17",
            },  # 负敞口脏数据
            {
                "exposure_id": "E004",
                "counterparty_id": "CP004",
                "gross_exposure_usd": 4500000,
                "net_exposure_usd": 3800000,
                "as_of_date": "2026-09-17",
            },
            {
                "exposure_id": "E005",
                "counterparty_id": "CP005",
                "gross_exposure_usd": 15000000,
                "net_exposure_usd": 12000000,
                "as_of_date": "2026-09-17",
            },
            {
                "exposure_id": "E006",
                "counterparty_id": "CP999",
                "gross_exposure_usd": 2100000,
                "net_exposure_usd": 1800000,
                "as_of_date": "2026-09-17",
            },  # 孤立外键
        ]
    )

    reg = pd.DataFrame(
        [
            {
                "counterparty_id": "CP001",
                "regulatory_class": "G-SIB",
                "basel_asset_class": "Sovereign/Bank",
                "reporting_required": True,
            },
            {
                "counterparty_id": "CP002",
                "regulatory_class": "Non-Bank Financial",
                "basel_asset_class": "Financial Institution",
                "reporting_required": True,
            },
            {
                "counterparty_id": "CP003",
                "regulatory_class": "Corporate Entity",
                "basel_asset_class": "Corporate",
                "reporting_required": True,
            },
            {
                "counterparty_id": "CP004",
                "regulatory_class": "Regional Bank",
                "basel_asset_class": "Sovereign/Bank",
                "reporting_required": False,
            },
            {
                "counterparty_id": "CP005",
                "regulatory_class": "Non-Bank Financial",
                "basel_asset_class": "Financial Institution",
                "reporting_required": True,
            },
        ]
    )

    integrated = exp.merge(cp, on="counterparty_id", how="left").merge(
        reg, on="counterparty_id", how="left"
    )
    return cp, exp, reg, integrated


cp, exp, reg, integrated = load_data()

# 3. 侧边栏导航
page = st.sidebar.radio(
    "Navigation Modules",
    [
        "1. Executive Overview",
        "2. Data Quality & Validation Engine",
        "3. Governance & Metadata Catalog",
        "4. AI Data Assistant",
        "5. Product Backlog & Roadmap",
    ],
)

# 模块 1： Executive Overview
if page == "1. Executive Overview":
    st.header("📊 Executive Data Product Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Data Quality", "94.2%", "+1.5% WoW")
    col2.metric("Completeness", "97.0%", "1 Missing Field")
    col3.metric("Validity Score", "95.0%", "1 Outlier Range")
    col4.metric("Integrity Flag", "1 Mismatch", "Orphan Foreign Key")
    st.markdown("---")
    st.subheader("Integrated Regulatory Data View")
    st.dataframe(integrated, use_container_width=True)

# 模块 2： Data Quality Engine
elif page == "2. Data Quality & Validation Engine":
    st.header("🔍 Automated Data Quality Engine")
    issues = []
    missing_ratings = cp[cp["credit_rating"].isna()]
    for idx, row in missing_ratings.iterrows():
        issues.append({
            "Rule": "Completeness",
            "Source Table": "counterparty",
            "Severity": "High",
            "Issue Description": (
                f"Missing Credit Rating for {row['counterparty_id']}"
            ),
        })
    invalid_exp = exp[exp["gross_exposure_usd"] < 0]
    for idx, row in invalid_exp.iterrows():
        issues.append({
            "Rule": "Validity Range",
            "Source Table": "exposure",
            "Severity": "Critical",
            "Issue Description": (
                f"Negative Gross Exposure (${row['gross_exposure_usd']}) for"
                f" {row['exposure_id']}"
            ),
        })
    orphans = exp[~exp["counterparty_id"].isin(cp["counterparty_id"])]
    for idx, row in orphans.iterrows():
        issues.append({
            "Rule": "Referential Integrity",
            "Source Table": "exposure",
            "Severity": "Critical",
            "Issue Description": (
                f"Unmapped Foreign Key {row['counterparty_id']} in Counterparty"
                " Master"
            ),
        })
    duplicates = cp[cp.duplicated(subset=["counterparty_id"])]
    for idx, row in duplicates.iterrows():
        issues.append({
            "Rule": "Uniqueness",
            "Source Table": "counterparty",
            "Severity": "Medium",
            "Issue Description": (
                f"Duplicate Primary Key detected for {row['counterparty_id']}"
            ),
        })
    st.error(f"🚨 Total Data Quality Exceptions Detected: {len(issues)}")
    st.table(pd.DataFrame(issues))

# 模块 3： Governance & Metadata
elif page == "3. Governance & Metadata Catalog":
    st.header("📚 Enterprise Governance & Data Catalog")
    tab1, tab2, tab3 = st.tabs(
        ["Business Glossary", "Data Ownership & Classification", "Data Lineage"]
    )
    with tab1:
        st.subheader("Business Glossary")
        st.markdown(
            "* **Counterparty**: A legal entity to which the firm has credit or"
            " financial exposure.\n* **Gross Exposure**: Aggregate financial"
            " exposure prior to applying eligible netting agreements.\n*"
            " **Net Exposure**: Residual credit exposure following netting and"
            " collateral adjustments."
        )
    with tab2:
        st.subheader("Data Ownership Matrix")
        metadata = [
            {
                "Field Name": "counterparty_id",
                "Domain": "Counterparty Master",
                "Business Owner": "Data Governance Office",
                "Data Classification": "Internal",
            },
            {
                "Field Name": "gross_exposure_usd",
                "Domain": "Risk Analytics",
                "Business Owner": "Enterprise Risk Management",
                "Data Classification": "Confidential",
            },
            {
                "Field Name": "credit_rating",
                "Domain": "Credit Risk",
                "Business Owner": "Credit Risk Office",
                "Data Classification": "Internal",
            },
        ]
        st.table(pd.DataFrame(metadata))
    with tab3:
        st.subheader("Data Lineage Pipeline")
        st.code(
            "[Source Systems] ---> [Raw Data Sources] ---> [Automated Quality"
            " Engine] ---> [Integrated Data Product] ---> [AI & Reporting Layer]"
        )

# 模块 4： AI Data Assistant
elif page == "4. AI Data Assistant":
    st.header("🤖 Enterprise Data AI Assistant")
    st.write(
        "Perform natural language queries against data quality rules,"
        " exceptions, and exposure metrics."
    )
    st.text_input(
        "Ask a question:", "Which counterparty records failed quality checks?"
    )
    if st.button("Run AI Query"):
        st.info("💡 **AI Assistant Insights:**")
        st.markdown(
            "* **CP003 (Crestline Partners)**: Failed **Completeness Check**"
            " (Missing Credit Rating).\n* **Exposure E003**: Failed **Validity"
            " Check** (Negative Gross Exposure: -$500,000).\n* **Exposure"
            " E006**: Failed **Referential Integrity Check** (Unmapped"
            " Counterparty ID `CP999`)."
        )

# 模块 5： Product Backlog & Roadmap
elif page == "5. Product Backlog & Roadmap":
    st.header("🎯 Product Strategy & Backlog Management")
    st.subheader("Capability Roadmap")
    st.markdown(
        "`Phase 1: Integration & Rules Engine` ➔ `Phase 2: Automated"
        " Governance` ➔ `Phase 3: GenAI Semantic Layer` "
    )
    st.subheader("Agile Backlog")
    backlog = [
        {
            "Epic": "EPIC-101 Data Integration",
            "User Story": (
                "As a Risk Analyst, I want consolidated counterparty exposures"
                " to support regulatory reporting."
            ),
            "Status": "Completed (POC)",
        },
        {
            "Epic": "EPIC-102 Quality Validation",
            "User Story": (
                "As a Data Quality Manager, I want automated rule engines to"
                " flag negative values and missing keys."
            ),
            "Status": "In Review",
        },
        {
            "Epic": "EPIC-103 AI Query Layer",
            "User Story": (
                "As an Executive, I want natural language Q&A interface across"
                " metadata and quality reports."
            ),
            "Status": "Backlog",
        },
    ]
    st.table(pd.DataFrame(backlog))
