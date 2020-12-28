import streamlit as st
import numpy as np

####Parameters
#Constant (Pi)
Pi              = np.pi

##Fabrication Parameters
#Baseline Process Node
#Unit: [nm]
Baseline_Process= 28.0

##Wafer Parameters
#Price per Wafer
#Unit: [US Dollar]
Wafer_Price     = 100.0

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
Price_Market    = 400

#Number of Units Installed
#Unit: [Units]
N_installation  = 1000000

#Market Share
#Unit:  [%]
Market_Share    = 25.0

#Sale Rate
#Unit:  [%]
Sale_Rate       = 85.0

#CAGR
#Unit: [%]
CAGR            = 35.5

##NRE Cost
#Cost for Tool Software
#Unit: [K US Dollar]
Cost_Tools      = 36000000.0/105.0

#Salary for Engineer per Year
#Unit: [US Dollar]
Engineer_Salary = 10000000.0

#Number of Engineers
#Units: [Persons]
Engineer_Workers= 6

##Design Parameters
#Chip Area
#Units: [mm**2]
Baseline_Chip_Area = 100.0


st.title('Cost Estimation')


##Market Parameters
st.subheader('Market Factors')

#Chip Price
price_market    = st.sidebar.slider('Price in Market [US Dollar]', 1, Price_Market*10, Price_Market)
st.text('Price in Market [US Dollar]    %s' % price_market)

#Number of Installations
number_of_installation = st.sidebar.slider('Installation in Market [Units]', 10000, N_installation*2, N_installation)
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
estimating_process = st.sidebar.slider('Process [nm]', 1.0, 45.0, Baseline_Process)
st.text('Estimating Process [nm]        %s' % estimating_process)

#Scaling Factor
scale_factor    = Baseline_Process / estimating_process
st.text('Scale Factor                   %s' % scale_factor)

#Scale Die Yeld
die_yield_factor= st.sidebar.slider('Die Yield Factor', 1.0, 15.0, Scale_Die_Yield)
st.text('Die Yield Factor               %s' % die_yield_factor)


##Design Parameters
st.subheader('Fabrication Factors')
#Chip Area
chip_area       = st.sidebar.slider('Chip Area [mm**2]', 1.0, 800.0, Baseline_Chip_Area)
st.text('Chip Area [mm**2]              %s' % chip_area)

#Available Maximum Number of Chips before Yielding
#Unit: Number of Chips
negative_factor = (Pi * wafer_diameter) / np.sqrt(2 * Pi * chip_area / (scale_factor**2))
num_chips       = int(np.floor((chip_area / (scale_factor**2) - negative_factor)))
st.text('Max Chips/Wafer [Chips]        %s' % num_chips)

#Number of Defect Chip
num_defect = st.sidebar.slider('Number of Defect Chips [Chips]', 1, num_chips, 1)
st.text('Defect Chips/Wafer [Chips]     %s' % num_defect)

defect_density  = float(chip_area) * float(num_defect) / float(wafer_area)
st.text('Defect Density [Defect/mm**2]  %s' % num_defect)

#Die Yield per Wafer
#Unit: [%]
die_yield       = num_chips / np.power((1 + defect_density * chip_area), die_yield_factor)
st.text('Die Yield/Wafer [Chips]        %s' % die_yield)

#Number of Available Chips after Yielding
#Unit: [Chips]
N_Chips_Yield   = int(np.floor(die_yield * num_chips))
st.text('Available Chips/Wafer [Chips]  %s' % N_Chips_Yield)

#Number of Wafers needed for Target Market Share
#Unit: [Wafers]
N_Wafer         = int(np.ceil((N_installation * market_share / 100.0) / N_Chips_Yield))
st.text('Number of Wafers [Wafers]      %s' % N_Wafer)

wafer_price     = st.sidebar.slider('Wafer Price [US Dollar]', 1.0, Wafer_Price*2.0, Wafer_Price)
st.text('Wafer Price [US Dollar]        %s' % wafer_price)

#Total Cost for Wafer
Cost_Total_Wafer= N_Wafer * wafer_price
st.text('Total Wafer Cost [US Dollar]   %s' % Cost_Total_Wafer)

#Chip Cost
Chip_Cost       = float(Cost_Total_Wafer) / float(N_Chips_Yield)
st.text('Total Chip Cost [US Dollar]    %s' % Chip_Cost)

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
Cost_Year       = Cost_Total_Wafer + (Cost_Test + Cost_Package) * N_Chips_Yield + Cost_NRE
st.text('Total Cost/Year [M US Dollar]    %s' % (Cost_Year / 1000000))

####Product Price
Total_Profit    = (price_market * number_of_installation * market_share * sales_rate) - Cost_Year
st.subheader('Total Profit/Year [M US Dollar]  %s' % (Total_Profit / 1000000))
