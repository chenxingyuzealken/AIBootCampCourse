import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.ticker as mticker


# Load the expenditure data (you can adjust the file path)
def load_expenditure_data():
    file_path = 'Singstat2018ExpenditureData.xlsx'  # Replace with your file path
    expenditure_data = pd.read_excel(file_path, skiprows=9)
    
    # Rename columns for easier access
    expenditure_data.columns = ['Type_of_Goods_and_Services', 'Total', 'Income_Quintile_1', 'Income_Quintile_2', 
                                'Income_Quintile_3', 'Income_Quintile_4', 'Income_Quintile_5']

    # Drop rows where 'Type_of_Goods_and_Services' is NaN
    expenditure_data = expenditure_data.dropna(subset=['Type_of_Goods_and_Services'])

    # Convert expenditure columns to numeric
    expenditure_data[['Total', 'Income_Quintile_1', 'Income_Quintile_2', 'Income_Quintile_3', 'Income_Quintile_4', 'Income_Quintile_5']] = expenditure_data[
        ['Total', 'Income_Quintile_1', 'Income_Quintile_2', 'Income_Quintile_3', 'Income_Quintile_4', 'Income_Quintile_5']].apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN values
    expenditure_data_cleaned = expenditure_data.dropna(subset=['Total', 'Income_Quintile_1', 'Income_Quintile_2', 'Income_Quintile_3', 'Income_Quintile_4', 'Income_Quintile_5'])
    return expenditure_data_cleaned

def map_life_simulator_to_expenditure(life_simulator_data, expenditure_data):
    category_mapping = {
        'food': ['FOOD AND NON-ALCOHOLIC BEVERAGES', 'FOOD SERVING SERVICES'],  # Updated to include both categories for food
        'transport': 'TRANSPORT',
        'travel': 'RECREATION AND CULTURE',
        'housing': 'Imputed Rental for Owner-Occupied Accommodation',
        'utilities': 'HOUSING AND UTILITIES',
        'healthcare': 'HEALTH',
        'education': 'EDUCATION',
        'personal_care': 'PERSONAL CARE',
        'communication': 'COMMUNICATION',
        'clothing': 'CLOTHING AND FOOTWEAR'
    }

    # Rename the income quintiles for easier understanding
    quintile_labels = {
        'Income_Quintile_1': 'Bottom 20% of Households',
        'Income_Quintile_2': 'Lower Middle 20% of Households',
        'Income_Quintile_3': 'Middle 20% of Households',
        'Income_Quintile_4': 'Upper Middle 20% of Households',
        'Income_Quintile_5': 'Top 20% of Households',
    }

    results = {}
    
    for life_category, expenditure_category in category_mapping.items():
        user_spending = life_simulator_data.get(life_category, 0)

        # Handle the case where food expense is a combination of two categories
        if life_category == 'food':
            rows = expenditure_data[expenditure_data['Type_of_Goods_and_Services'].isin(expenditure_category)]
            total_row = rows.sum(numeric_only=True) if not rows.empty else None
        else:
            rows = expenditure_data[expenditure_data['Type_of_Goods_and_Services'] == expenditure_category]
            total_row = rows.iloc[0] if not rows.empty else None

        if total_row is not None:  # Only proceed if the category exists in the dataset
            quintile_comparison = {
                quintile_labels['Income_Quintile_1']: total_row['Income_Quintile_1'],
                quintile_labels['Income_Quintile_2']: total_row['Income_Quintile_2'],
                quintile_labels['Income_Quintile_3']: total_row['Income_Quintile_3'],
                quintile_labels['Income_Quintile_4']: total_row['Income_Quintile_4'],
                quintile_labels['Income_Quintile_5']: total_row['Income_Quintile_5'],
            }
            
            closest_income_quintile = min(quintile_comparison, key=lambda k: abs(quintile_comparison[k] - user_spending))
            
            results[life_category] = {
                'user_spending': user_spending,
                'closest_income_quintile': closest_income_quintile,
                'spending_for_quintile': quintile_comparison[closest_income_quintile]
            }

    return results


# Function to handle user input in Life Simulator, including retirement planning components
def get_user_input():
    st.title("Lifestyle and Retirement Adequacy Simulator")
    st.write("Simulate financial planning at different life stages for a Singaporean after the age of 20.")

    # Inputs for user information
    age = st.slider("Select your current age", 20, 100, step=1)  # Capture the age correctly
    income = st.number_input("Enter your annual income (SGD)", min_value=0, value=50000, step=1000)
    savings = st.number_input("Enter your current savings (SGD)", min_value=0, value=10000, step=1000)
    
    # Retirement planning components
    retirement_age = st.slider("At what age do you plan to retire?", 55, 70, step=1, value=65)
    post_retirement_expenses = st.number_input("Estimate your monthly post-retirement expenses (SGD)", min_value=0, value=2000, step=100)
    savings_growth_rate = st.slider("Expected annual growth rate on savings (%)", 0.0, 10.0, step=0.1, value=3.0)
    life_expectancy = st.slider("Expected life expectancy (years)", 70, 100, step=1, value=85)
    
    # CPF related inputs
    current_cpf_savings = st.number_input("Enter your current CPF savings (SGD)", min_value=0, value=100000, step=1000)
    cpf_contribution_rate = st.slider("Expected CPF contribution rate (%)", 0.0, 37.0, step=0.5, value=37.0)
    
    # Input fields for various expenditures
    transport_cost = st.number_input("Enter your monthly transport cost (SGD)", min_value=0, value=150, step=10)
    food_cost = st.number_input("Enter your monthly food cost (SGD)", min_value=0, value=500, step=50)
    travel_cost = st.number_input("Enter your yearly travel cost (SGD)", min_value=0, value=3000, step=500)
    housing_cost = st.number_input("Enter your monthly housing cost (SGD)", min_value=0, value=1500, step=100)
    utilities_cost = st.number_input("Enter your monthly utilities cost (SGD)", min_value=0, value=200, step=50)
    healthcare_cost = st.number_input("Enter your monthly healthcare cost (SGD)", min_value=0, value=300, step=50)
    education_cost = st.number_input("Enter your yearly education cost (SGD)", min_value=0, value=2000, step=500)
    personal_care_cost = st.number_input("Enter your monthly personal care cost (SGD)", min_value=0, value=100, step=20)
    communication_cost = st.number_input("Enter your monthly communication cost (SGD)", min_value=0, value=80, step=10)
    clothing_cost = st.number_input("Enter your yearly clothing and footwear cost (SGD)", min_value=0, value=600, step=100)

    # Collect user spending data
    life_simulator_data = {
        'age': age,  # Ensure age is captured
        'income': income,
        'savings': savings,
        'retirement_age': retirement_age,
        'post_retirement_expenses': post_retirement_expenses,
        'savings_growth_rate': savings_growth_rate,
        'life_expectancy': life_expectancy,
        'current_cpf_savings': current_cpf_savings,
        'cpf_contribution_rate': cpf_contribution_rate,
        'food': food_cost,
        'transport': transport_cost,
        'travel': travel_cost,
        'housing': housing_cost,
        'utilities': utilities_cost,
        'healthcare': healthcare_cost,
        'education': education_cost,
        'personal_care': personal_care_cost,
        'communication': communication_cost,
        'clothing': clothing_cost
    }
    
    return life_simulator_data

######################
# Function to plot savings growth and withdrawals in a line chart
import matplotlib.ticker as mticker

def plot_savings_projection_with_withdrawals(life_simulator_data, retirement_plan):
    current_age = life_simulator_data['age']
    retirement_age = life_simulator_data['retirement_age']
    life_expectancy = life_simulator_data['life_expectancy']
    years_until_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    # Simulate savings growth until retirement
    savings = life_simulator_data['savings']
    cpf_savings = life_simulator_data['current_cpf_savings']
    growth_rate = life_simulator_data['savings_growth_rate'] / 100
    savings_over_time = []
    cpf_over_time = []
    
    # CPF contributions and savings growth until retirement
    for year in range(years_until_retirement):
        annual_cpf_contributions = life_simulator_data['income'] * life_simulator_data['cpf_contribution_rate'] / 100
        cpf_savings += annual_cpf_contributions  # CPF contributions every year
        cpf_savings *= (1 + growth_rate)  # CPF grows every year
        savings *= (1 + growth_rate)  # Personal savings grow every year
        cpf_over_time.append(cpf_savings)
        savings_over_time.append(savings)

    # Combine CPF and savings
    total_savings = [s + c for s, c in zip(savings_over_time, cpf_over_time)]

    # Simulate withdrawals after retirement
    monthly_withdrawal = retirement_plan['monthly_withdrawal']
    for year in range(years_in_retirement):
        total_savings[-1] -= monthly_withdrawal * 12  # Subtract yearly withdrawal
        total_savings.append(max(total_savings[-1], 0))  # Ensure savings don't go negative

    # Create the timeline (age)
    ages = list(range(current_age, current_age + len(total_savings)))

    # Plot savings projection
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ages, total_savings, label="Total Savings (CPF + Personal)", color='green', linewidth=2)
    ax.axvline(retirement_age, color='red', linestyle='--', linewidth=1.5, label="Retirement Age")
    ax.axhline(0, color='black', linewidth=0.5)

    # Highlight the withdrawal period with annotation
    if years_in_retirement > 0:
        ax.fill_between(ages[years_until_retirement:], total_savings[years_until_retirement:], color='lightcoral', alpha=0.3, label="Withdrawal Period")
        ax.text(retirement_age + 1, monthly_withdrawal * 12, f"Monthly Withdrawal: SGD {monthly_withdrawal:,.0f}", color='red', fontsize=10)

    # Fill under the curve for total savings visualization
    ax.fill_between(ages, total_savings, color='lightgreen', alpha=0.4)

    # Labels and title
    ax.set_xlabel("Age")
    ax.set_ylabel("Total Savings (SGD)")
    ax.set_title("Retirement Savings Projection with Withdrawals")
    ax.legend()

    # Set Y-axis limit to cap large values for readability
    max_y = max(total_savings) * 1.1  # Add a small margin above the max value
    ax.set_ylim(0, max_y)

    # Turn off scientific notation on the Y-axis
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    # Optionally format large numbers with commas for better readability
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Show plot in Streamlit
    st.pyplot(fig)



# Function to calculate if the user can sustain their lifestyle during retirement
def calculate_retirement_sustainability(life_simulator_data):
    current_age = life_simulator_data['age']
    retirement_age = life_simulator_data['retirement_age']
    post_retirement_expenses = life_simulator_data['post_retirement_expenses']
    savings_growth_rate = life_simulator_data['savings_growth_rate'] / 100  # Convert to decimal
    current_cpf_savings = life_simulator_data['current_cpf_savings']
    cpf_contribution_rate = life_simulator_data['cpf_contribution_rate'] / 100  # Convert to decimal
    life_expectancy = life_simulator_data['life_expectancy']
    annual_income = life_simulator_data['income']
    current_savings = life_simulator_data['savings']
    
    # Calculate the number of years before retirement and the number of years post-retirement
    years_until_retirement = retirement_age - current_age
    years_of_retirement = life_expectancy - retirement_age
    
    # CPF contributions until retirement
    annual_cpf_contributions = annual_income * cpf_contribution_rate
    total_cpf_contributions_until_retirement = annual_cpf_contributions * years_until_retirement

    # Total savings at the time of retirement (CPF savings + personal savings)
    total_savings_at_retirement = current_savings + current_cpf_savings + total_cpf_contributions_until_retirement

    # Apply savings growth rate until retirement
    total_savings_at_retirement *= (1 + savings_growth_rate) ** years_until_retirement
    
    # Project total post-retirement expenses based on actual expected expenses
    total_post_retirement_expenses = post_retirement_expenses * 12 * years_of_retirement
    
    # Ensure that the monthly withdrawal is based on the user's actual post-retirement expenses
    monthly_withdrawal = post_retirement_expenses  # This should reflect their actual monthly cost

    # Determine if the user's savings can support their lifestyle during retirement
    if total_savings_at_retirement >= total_post_retirement_expenses:
        return {
            'status': 'Sustainable',
            'total_savings_at_retirement': total_savings_at_retirement,
            'total_post_retirement_expenses': total_post_retirement_expenses,
            'monthly_withdrawal': monthly_withdrawal,  # Return the correct monthly withdrawal
            'message': 'Your retirement plan is sustainable. You have enough savings to cover your expenses.'
        }
    else:
        return {
            'status': 'Not Sustainable',
            'total_savings_at_retirement': total_savings_at_retirement,
            'total_post_retirement_expenses': total_post_retirement_expenses,
            'monthly_withdrawal': monthly_withdrawal,  # Return the correct monthly withdrawal
            'message': 'Your retirement plan is not sustainable. You may run out of savings before your estimated lifespan.'
        }
    


######################

def life_simulator():
    expenditure_data = load_expenditure_data()  # Load expenditure data

    life_simulator_data = get_user_input()  # Get user inputs
    
    # Compare user's spending to the expenditure data
    comparison_results = map_life_simulator_to_expenditure(life_simulator_data, expenditure_data)
    
    # Display spending comparison results
    st.subheader("Comparison to Average Household Expenditure")
    for category, result in comparison_results.items():
        st.write(f"Category: {category.capitalize()}")
        st.write(f"- Your Spending: SGD {result['user_spending']}")
        st.write(f"- Closest Income Group: {result['closest_income_quintile']}")
        st.write(f"- Average Spending in this Group: SGD {result['spending_for_quintile']}")
        st.write("")


    # Calculate and display retirement sustainability check
    retirement_plan = calculate_retirement_sustainability(life_simulator_data)
    st.subheader("Retirement Sustainability Check")
    st.write(f"Total Savings at Retirement: SGD {retirement_plan['total_savings_at_retirement']:,}")
    st.write(f"Total Expected Post-Retirement Expenses: SGD {retirement_plan['total_post_retirement_expenses']:,}")
    st.write(retirement_plan['message'])

    # Visualize savings projection with withdrawals
    plot_savings_projection_with_withdrawals(life_simulator_data, retirement_plan)

# Directly call the function in the script's main block
if __name__ == "__main__":
    life_simulator()

