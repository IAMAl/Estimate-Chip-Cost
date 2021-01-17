import streamlit as st
import numpy as np

####Parameters
#Constant (Pi)
Pi              = np.pi

##Fabrication Parameters
#Baseline Process Node
#Unit: [nm]
Baseline_Process= 5.0

##Wafer Parameters
#Price per Wafer
#Unit: [US Dollar]
Wafer_Price     = {'90':1650, '65':1937, '40':2274, '28':2891, '16':3984, '12':3984, '10':5992, '7':9346, '5':16988}

#Wafer Scale (Diameter)
#Unit: mm
Wafer_Diameter  = 300.0

#Coefficient to Scale Die-Yield
#Unit: [N/A]
Scale_Die_Yield = 10.0

#Number of Defect Chips
#Unit: [Chips]
N_Defect        = 1


##Fabrication Parameters
#Test Cost per Chip
#Unit: [US Dollar]
Cost_Test       = 5

#Packaging Cost per Chip
#Unit: [US Dollar]
Cost_Package    = 2


##Market Parameters
#Average Price in Market
#Unit: [US Dollar]
Price_Market    = 10

#Number of Units Installed
#Unit: [Units]
N_installation  = 1000000

#Market Share
#Unit:  [%]
Market_Share    = 10.0

#Sale Rate
#Unit:  [%]
Sale_Rate       = 85.0

#CAGR
#Unit: [%]
CAGR            = 20.0

##NRE Cost
#Cost for Tool Software
#Unit: [K US Dollar]
Cost_Tools      = 360000.0

#Salary for Engineer per Year
#Unit: [US Dollar]
Engineer_Salary = 120000.0

#Number of Engineers
#Units: [Persons]
Engineer_Workers= 10

##Design Parameters
#Chip Area
#Units: [mm**2]
Baseline_Chip_Area = 100.0


st.title('Cost Estimation')


##Market Parameters
st.subheader('Market Factors')

#Chip Price
price_market    = st.sidebar.slider('Price in Market [US Dollar]', 10, Price_Market*500, Price_Market)
st.text('Price in Market [US Dollar]    %s' % price_market)

#Number of Installations
number_of_installation = st.sidebar.slider('Installation in Market [Units]', 1000, N_installation*2, N_installation)
st.text('Installation in Market [Units] %s' % number_of_installation)

#Market Volume
volume_market   = price_market * number_of_installation
st.text('Market Volume [US Dollar]      %s' % volume_market)

#Compound Average Growth Rate (CAGR: Prediction Number)
#Unit: [%]
cagr            = st.sidebar.slider('Compound Average Growth Rate (CAGR) [%]', 2.5, 100.0, CAGR)
st.text('CAGR [Percent]                 %s' % cagr)

market_share    = st.sidebar.slider('Market Share [%]', 0.0, 100.0, Market_Share)
st.text('Market Share [Percent]         %s' % market_share)

#Sale Rate
sales_rate      = st.sidebar.slider('Sale Rate [%]', 0.0, 100.0, Sale_Rate)
st.text('Sale Rate [Percent]            %s' % sales_rate)


##Semiconductor Fabrication Parameters
st.subheader('Semiconductor Factors')
#Wafer Diameter
wafer_diameter  = st.sidebar.slider('Wafer Diameter [mm]', 200.0, Wafer_Diameter, Wafer_Diameter)
st.text('Wafer Diameter [mm]            %s' % wafer_diameter)

#Wafer Area
#Unit: [mm**2]
wafer_area      = Pi * ((wafer_diameter)**2.0)/4
st.text('Wafer Area [mm**2]             %s' % wafer_area)

#Estimating Process
Process_Node = st.sidebar.radio("Process Node [nm]", ('90', '65', '40', '28', '16', '12', '10', '7', '5'))
estimating_process = 5
if Process_Node == '90':
    estimating_process = 90
elif Process_Node == '65':
    estimating_process = 65
elif Process_Node == '40':
    estimating_process = 40
elif Process_Node == '28':
    estimating_process = 28
elif Process_Node == '16':
    estimating_process = 65
elif Process_Node == '12':
    estimating_process = 12
elif Process_Node == '7':
    estimating_process = 7

#Scale Die Yeld
die_yield_factor= st.sidebar.slider('Die Yield Factor', 1.0, 15.0, Scale_Die_Yield)
st.text('Die Yield Factor               %s' % die_yield_factor)


##Design Parameters
st.subheader('Fabrication Factors')
#Chip Area
die_area       = st.sidebar.slider('Chip Area [mm**2]', 1.0, 900.0, Baseline_Chip_Area)
st.text('Die Area [mm**2]               %s' % die_area)

#Available Maximum Number of Chips before Yielding
#Unit: Number of Chips
negative_factor = (Pi * wafer_diameter) / np.sqrt(2 * Pi * die_area)
num_chips       = int(np.floor((wafer_area/die_area - negative_factor)))
st.text('Max Dies/Wafer [Dies]          %s' % num_chips)

#Number of Defect Chip
num_defect = st.sidebar.slider('Number of Defect Dies [Dies]', 1, num_chips, 1)
st.text('Defect Dies/Wafer [Dies]       %s' % num_defect)

defect_density  = float(die_area) * float(num_defect) / float(wafer_area)
st.text('Defect Density [Defect/mm**2]  %s' % defect_density)

#Die Yield per Wafer
#Unit: [%]
die_yield       = (num_chips - num_defect) / num_chips
st.text('Die Yield/Wafer [Percentage]   %s' % die_yield)

#Number of Available Chips after Yielding
#Unit: [Chips]
N_Die_Yield   = int(np.floor(die_yield * num_chips))
st.text('Available Dies/Wafer [Dies]    %s' % N_Die_Yield)

#Number of Wafers needed for Target Market Share
#Unit: [Wafers]
N_Wafer         = int(np.ceil((N_installation * market_share / 100.0) / N_Die_Yield))
st.text('Number of Wafers [Wafers]      %s' % N_Wafer)

wafer_price     = Wafer_Price[Process_Node]
st.text('Wafer Price [US Dollar]        %s' % wafer_price)

#Total Cost for Wafer
Cost_Total_Wafer= N_Wafer * wafer_price
st.text('Total Wafer Cost [US Dollar]   %s' % Cost_Total_Wafer)

#Die Cost
Die_Cost        = float(Cost_Total_Wafer) / float(N_Die_Yield)
st.text('Total Die Cost [US Dollar]     %s' % Die_Cost)

####NRE Cost Parameters
st.subheader('NRE Cost Factors')

#Cost for Tool
cost_tools      = st.sidebar.slider('Tool Cost [K US Dollar]', 0, int(Cost_Tools*1.25), int(Cost_Tools))
st.text('Tool Cost [US Dollar]          %s' % cost_tools)

#Number of Engineers
num_engineers   = st.sidebar.slider('Engineers', 1, 50, Engineer_Workers)
st.text('Number of Engineers            %s' % num_engineers)

#Salary for Engineer per Year
Engineer_Salary = st.sidebar.slider('Engineer Salary [K US Dollar]', Engineer_Salary/2, Engineer_Salary*3, Engineer_Salary)
st.text('Engineer Salary [US Dollar]    %s' % Engineer_Salary)

#Worker Fees
#Fees per Year
Cost_Engineer   = num_engineers * Engineer_Salary
st.text('Total Salary [US Dollar]       %s' % Cost_Engineer)

#Total NRE Cost
Cost_NRE        = cost_tools + Cost_Engineer
st.text('Total NRE Cost [US Dollar]     %s' % (Cost_NRE))

####Total Cost
st.subheader('Total Cost')
#Cost per Year
Cost_Year       = Cost_Total_Wafer + (Cost_Test + Cost_Package) * N_Die_Yield + Cost_NRE
st.text('Total Cost/Year [M US Dollar]    %s' % (Cost_Year / 1000000))

####Product Price
Total_Profit    = (price_market * number_of_installation * market_share * sales_rate) - Cost_Year
st.subheader('Total Profit/Year [M US Dollar]  %s' % (Total_Profit / 1000000))
