import pandas as pd 


class TimeSeriesGeneration():
    def __init__(self , start_date , end_date) -> None:
        self.start_date = start_date
        self.end_date = end_date


    def generate(self , freq):
        """
        Generate a time index (DatetimeIndex) with the specified frequency.

        Parameters:
            start_date (datetime): The start date of the time index.
            end_date (datetime): The end date of the time index.
            freq (str): The frequency for the time index (e.g., '10T' for 10 minutes, '1H' for hourly, 'D' for daily).

        Returns:
            DatetimeIndex: The generated time index.
        """
        date_rng = pd.date_range(start=self.start_date, end=self.end_date,
                                  freq=freq)
        return date_rng



