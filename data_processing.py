import pandas as pd

svcgdata = pd.read_csv('downloaded_samples/unprocessed_consolidated_sample_svcg_file.csv', delimiter=",", 
                       header=None, index_col=False, names=["LoanSequenceNumber",
                        "MonthlyReportingPeriod",
                        "CurrentActualUPB",
                        "CurrentLoanDelinquencyStatus",
                        "LoanAge",
                        "RemainingMonthsLegalMaturity",
                        "DefectSettlementDate",
                        "ModificationFlag",
                        "ZeroBalanceCode",
                        "ZeroBalanceEffectiveDate",
                        "CurrentInterestRate",
                        "CurrentDeferredUPB",
                        "DDLPI",
                        "MIRecoveries",
                        "NetSalesProceeds",
                        "NonMIRecoveries",
                        "Expenses",
                        "LegalCosts",
                        "MaintenancePreservationCosts",
                        "TaxesInsurance",
                        "MiscellaneousExpenses",
                        "ActualLossCalculation",
                        "ModificationCost",
                        "StepModificationFlag",
                        "DeferredPaymentPlan",
                        "ELTV",
                        "ZeroBalanceRemovalUPB",
                        "DelinquentAccruedInterest",
                        "DelinquencyDueDisaster",
                        "BorrowerAssistanceStatusCode",
                        "CurrentMonthModificationCost",
                        "InterestBearingUPB"])

print(svcgdata.shape)

# Focus only on the needed columns (analysis will be based mostly on orgination data)
svcgdata = svcgdata[["LoanSequenceNumber",
    "MonthlyReportingPeriod",
    "CurrentLoanDelinquencyStatus",
    "ZeroBalanceCode",
    "ZeroBalanceEffectiveDate"]]
print(svcgdata.shape)

svcgdata[['ZeroBalanceCode']] = svcgdata[['ZeroBalanceCode']].fillna(0)
svcgdata['ZeroBalanceCode'] = svcgdata['ZeroBalanceCode'].astype('int')
svcgdata['ZeroBalanceCode'].unique()

svcgdata['CurrentLoanDelinquencyStatus'].isnull().values.any()
svcgdata['CurrentLoanDelinquencyStatus'].unique()
svcgdata['CurrentLoanDelinquencyStatus'].loc[(svcgdata['CurrentLoanDelinquencyStatus'] == 'RA')] = 1111
svcgdata['CurrentLoanDelinquencyStatus'] = svcgdata['CurrentLoanDelinquencyStatus'].astype('int')

svcgdata['CurrentLoanDelinquencyStatus'].unique()

svcgdata[['ZeroBalanceEffectiveDate']] = svcgdata[['ZeroBalanceEffectiveDate']].fillna(999999)
svcgdata['ZeroBalanceEffectiveDate'] = svcgdata['ZeroBalanceEffectiveDate'].astype('int')
svcgdata['ZeroBalanceEffectiveDate'].unique()

svcgdata.dropna(subset=['LoanSequenceNumber'], inplace=True)
svcgdata.isnull().values.any()
print(svcgdata.dtypes)
print(svcgdata.groupby('ZeroBalanceCode')['LoanSequenceNumber'].count())

origdata = pd.read_csv('downloaded_samples/unprocessed_consolidated_sample_orig_file.csv', delimiter=",", 
                       header=None, index_col=False, names=["CreditScore",
                                                            "FirstPaymentDate",
                                                            "FirstTimeHomebuyerFlag",
                                                            "MaturityDate",
                                                            "MSA",
                                                            "MI",
                                                            "NumberUnits",
                                                            "OccupancyStatus",
                                                            "OriginalCLTV",
                                                            "OriginalDTI",
                                                            "OriginalUPB",
                                                            "OriginalLTV",
                                                            "OriginalInterestRate",
                                                            "Channel",
                                                            "PPMFlag",
                                                            "AmortizationType",
                                                            "PropertyState",
                                                            "PropertyType",
                                                            "PostalCode",
                                                            "LoanSequenceNumber",
                                                            "LoanPurpose",
                                                            "OriginalLoanTerm",
                                                            "NumberBorrowers",
                                                            "SellerName",
                                                            "ServicerName",
                                                            "SuperConformingFlag",
                                                            "PreHARPLoanSequenceNumber",
                                                            "ProgramIndicator",
                                                            "HARPIndicator",
                                                            "PropertyValuationMethod",
                                                            "InterestOnlyIndicator"], 
                       low_memory = False)

origdata['Year'] = ['20'+ x for x in (origdata['LoanSequenceNumber'].apply(lambda x: x[1:3]))]
origdata[['Year']] = origdata[['Year']].astype('int')

origdata[['MSA']]=origdata[['MSA']].fillna(0)
origdata[['MSA']] = origdata[['MSA']].astype('int')

origdata[['SuperConformingFlag']]=origdata[['SuperConformingFlag']].fillna(0)
origdata['SuperConformingFlag'].loc[(origdata['SuperConformingFlag'] == 'Y')] = 1
origdata[['SuperConformingFlag']] = origdata[['SuperConformingFlag']].astype('int')

origdata[["PreHARPLoanSequenceNumber"]]=origdata[["PreHARPLoanSequenceNumber"]].fillna(0)

origdata[['HARPIndicator']]=origdata[['HARPIndicator']].fillna(0)
origdata['HARPIndicator'].loc[(origdata['HARPIndicator'] == 'Y')] = 1
origdata[['HARPIndicator']] = origdata[['HARPIndicator']].astype('int')

origdata['MaturityDate'].unique()
origdata['MaturityDate'].loc[(origdata['MaturityDate'] == '.')] = 999999
origdata[['MaturityDate']] = origdata[['MaturityDate']].astype('int')

origdata.info()

merged_df = pd.merge(svcgdata,origdata,on="LoanSequenceNumber", how="left")
merged_df.to_csv('data_all.csv', index=False)