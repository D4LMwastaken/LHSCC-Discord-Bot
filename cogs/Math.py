"""
Math Cog for Discord Bot
This module provides mathematical and statistical operations for AP PreCalc and AP Statistics.
It includes basic arithmetic, trigonometry, and statistical analysis functions.

Dependencies:
- numpy: For numerical computations and statistical functions
- scipy.stats: For advanced statistical operations
- math/cmath: For mathematical operations including complex numbers
"""

import cmath
import math
import textwrap
import discord
from discord import app_commands
from discord.ext import commands
import numpy as np
from scipy import stats

async def send_long_message(interaction: discord.Interaction, content: str):
    """
    Utility function to send messages that might exceed Discord's 2000 character limit.
    Splits long messages into chunks and sends them sequentially.
    
    Args:
        interaction: Discord interaction object
        content: The message content to send
    """
    if len(content) <= 2000:
        await interaction.response.send_message(content)
        return

    chunks = textwrap.wrap(content, width=1990, replace_whitespace=False)
    await interaction.response.send_message(chunks[0])

    for chunk in chunks[1:]:
        await interaction.followup.send(chunk)

class Math(commands.Cog):
    """
    A cog that provides mathematical and statistical operations through Discord slash commands.
    Includes functionality for both AP PreCalc and AP Statistics coursework.
    """
    
    def __init__(self, bot):
        self.bot = bot

    math_group = app_commands.Group(name="math", description="Advanced mathematical operations")

    @math_group.command(name="add", description="Add two numbers")
    async def add(self, interaction: discord.Interaction, num1: float, num2: float):
        """
        Add two numbers together.
        
        Args:
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 + num2
            await interaction.response.send_message(f"{num1} + {num2} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="subtract", description="Subtract two numbers")
    async def subtract(self, interaction: discord.Interaction, num1: float, num2: float):
        """
        Subtract the second number from the first.
        
        Args:
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 - num2
            await interaction.response.send_message(f"{num1} - {num2} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="multiply", description="Multiply two numbers")
    async def multiply(self, interaction: discord.Interaction, num1: float, num2: float):
        """
        Multiply two numbers together.
        
        Args:
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 * num2
            await interaction.response.send_message(f"{num1} × {num2} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="divide", description="Divide two numbers")
    async def divide(self, interaction: discord.Interaction, num1: float, num2: float):
        """
        Divide the first number by the second.
        
        Args:
            num1: The dividend
            num2: The divisor
        """
        try:
            if num2 == 0:
                await interaction.response.send_message("Cannot divide by zero!")
                return
            result = num1 / num2
            await interaction.response.send_message(f"{num1} ÷ {num2} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="power", description="Calculate a number raised to a power")
    async def power(self, interaction: discord.Interaction, base: float, exponent: float):
        """
        Calculate the result of raising a number to a power.
        
        Args:
            base: The base number
            exponent: The exponent
        """
        try:
            result = math.pow(base, exponent)
            await interaction.response.send_message(f"{base}^{exponent} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="sqrt", description="Calculate the square root of a number")
    async def sqrt(self, interaction: discord.Interaction, number: float):
        """
        Calculate the square root of a number.
        
        Args:
            number: The number to find the square root of
        """
        try:
            if number < 0:
                result = cmath.sqrt(number)
                await interaction.response.send_message(f"√{number} = {result} (complex number)")
            else:
                result = math.sqrt(number)
                await interaction.response.send_message(f"√{number} = {result}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="sin", description="Calculate sine (in degrees)")
    async def sin(self, interaction: discord.Interaction, angle: float):
        """
        Calculate the sine of an angle in degrees.
        
        Args:
            angle: The angle in degrees
        """
        try:
            result = math.sin(math.radians(angle))
            await interaction.response.send_message(f"sin({angle}°) = {result:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="cos", description="Calculate cosine (in degrees)")
    async def cos(self, interaction: discord.Interaction, angle: float):
        """
        Calculate the cosine of an angle in degrees.
        
        Args:
            angle: The angle in degrees
        """
        try:
            result = math.cos(math.radians(angle))
            await interaction.response.send_message(f"cos({angle}°) = {result:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="tan", description="Calculate tangent (in degrees)")
    async def tan(self, interaction: discord.Interaction, angle: float):
        """
        Calculate the tangent of an angle in degrees.
        
        Args:
            angle: The angle in degrees
        """
        try:
            if abs(math.cos(math.radians(angle))) < 1e-10:
                await interaction.response.send_message("Error: tangent is undefined at this angle")
                return
            result = math.tan(math.radians(angle))
            await interaction.response.send_message(f"tan({angle}°) = {result:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="log", description="Calculate logarithm with custom base")
    async def log(self, interaction: discord.Interaction, number: float, base: float | None = None):
        """
        Calculate the logarithm of a number with a custom base.
        
        Args:
            number: The number to find the logarithm of
            base: The base of the logarithm (default is 10)
        """
        try:
            if base is None:
                base = 10.0
            if number <= 0 or base <= 0 or base == 1:
                await interaction.response.send_message("Error: Invalid input for logarithm")
                return
            result = math.log(number, base)
            await interaction.response.send_message(f"log_{base}({number}) = {result:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="ln", description="Calculate natural logarithm")
    async def ln(self, interaction: discord.Interaction, number: float):
        """
        Calculate the natural logarithm of a number.
        
        Args:
            number: The number to find the natural logarithm of
        """
        try:
            if number <= 0:
                await interaction.response.send_message("Error: Cannot calculate natural logarithm of non-positive number")
                return
            result = math.log(number)
            await interaction.response.send_message(f"ln({number}) = {result:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="area_circle", description="Calculate area of a circle")
    async def area_circle(self, interaction: discord.Interaction, radius: float):
        """
        Calculate the area of a circle.
        
        Args:
            radius: The radius of the circle
        """
        try:
            if radius < 0:
                await interaction.response.send_message("Error: Radius cannot be negative")
                return
            area = math.pi * radius * radius
            await interaction.response.send_message(f"Area of circle with radius {radius} = {area:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="area_triangle", description="Calculate area of a triangle using base and height")
    async def area_triangle(self, interaction: discord.Interaction, base: float, height: float):
        """
        Calculate the area of a triangle using the base and height.
        
        Args:
            base: The base of the triangle
            height: The height of the triangle
        """
        try:
            if base < 0 or height < 0:
                await interaction.response.send_message("Error: Dimensions cannot be negative")
                return
            area = 0.5 * base * height
            await interaction.response.send_message(f"Area of triangle with base {base} and height {height} = {area:.4f}")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="mean", description="Calculate arithmetic mean of numbers (separate with spaces)")
    async def mean(self, interaction: discord.Interaction, *, numbers: str):
        """
        Calculate the arithmetic mean of a set of numbers.
        
        Args:
            numbers: Space-separated list of numbers
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers to calculate mean")
                return
            result = sum(nums) / len(nums)
            message = f"Numbers provided: {nums}\nMean = {result:.4f}\n"
            message += f"\nDetailed calculation:\nSum = {sum(nums)}\nCount = {len(nums)}\nMean = Sum/Count = {result:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="quadratic", description="Solve quadratic equation ax² + bx + c = 0")
    async def quadratic(self, interaction: discord.Interaction, a: float, b: float, c: float):
        """
        Solve a quadratic equation of the form ax² + bx + c = 0.
        
        Args:
            a: The coefficient of the squared term
            b: The coefficient of the linear term
            c: The constant term
        """
        try:
            if a == 0:
                await interaction.response.send_message("Error: Not a quadratic equation (a = 0)")
                return
            
            discriminant = b**2 - 4*a*c
            
            if discriminant > 0:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                await interaction.response.send_message(f"Two real solutions:\nx₁ = {x1:.4f}\nx₂ = {x2:.4f}")
            elif discriminant == 0:
                x = -b / (2*a)
                await interaction.response.send_message(f"One real solution:\nx = {x:.4f}")
            else:
                real = -b / (2*a)
                imag = math.sqrt(-discriminant) / (2*a)
                await interaction.response.send_message(
                    f"Two complex solutions:\n"
                    f"x₁ = {real:.4f} + {imag:.4f}i\n"
                    f"x₂ = {real:.4f} - {imag:.4f}i"
                )
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="median", description="Calculate median of numbers (separate with spaces)")
    async def median(self, interaction: discord.Interaction, *, numbers: str):
        """
        Calculate the median (middle value) of a dataset.
        Example usage: /math median 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers to calculate median")
                return
            result = np.median(nums)
            message = f"Numbers provided: {nums}\nMedian = {result:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="mode", description="Calculate mode of numbers (separate with spaces)")
    async def mode(self, interaction: discord.Interaction, *, numbers: str):
        """
        Find the mode (most frequent value) in a dataset.
        Example usage: /math mode 1 2 2 3 3 3 4
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers to calculate mode")
                return
            mode_result = stats.mode(nums)
            message = f"Numbers provided: {nums}\nMode = {mode_result.mode[0]:.4f} (occurs {mode_result.count[0]} times)"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="std_dev", description="Calculate standard deviation (separate numbers with spaces)")
    async def std_dev(self, interaction: discord.Interaction, *, numbers: str):
        """
        Calculate the sample standard deviation of a dataset.
        Uses n-1 degrees of freedom (Bessel's correction).
        Example usage: /math std_dev 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers to calculate standard deviation")
                return
            result = np.std(nums, ddof=1)  # ddof=1 for sample standard deviation
            message = f"Numbers provided: {nums}\nStandard Deviation = {result:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="variance", description="Calculate variance (separate numbers with spaces)")
    async def variance(self, interaction: discord.Interaction, *, numbers: str):
        """
        Calculate the sample variance of a dataset.
        Uses n-1 degrees of freedom (Bessel's correction).
        Example usage: /math variance 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers to calculate variance")
                return
            result = np.var(nums, ddof=1)  # ddof=1 for sample variance
            message = f"Numbers provided: {nums}\nVariance = {result:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="z_score", description="Calculate z-score for a value in a dataset")
    async def z_score(self, interaction: discord.Interaction, value: float, *, numbers: str):
        """
        Calculate the z-score (standard score) for a value within a dataset.
        Z-score represents how many standard deviations away from the mean a value is.
        Example usage: /math z_score 75 70 80 85 90 75 80
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide a dataset")
                return
            mean = np.mean(nums)
            std = np.std(nums, ddof=1)
            z = (value - mean) / std
            message = f"Value: {value}\nDataset: {nums}\nZ-score = {z:.4f}\n"
            message += f"\nCalculation details:\nMean = {mean:.4f}\nStandard Deviation = {std:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="correlation", description="Calculate Pearson correlation coefficient (x y pairs)")
    async def correlation(self, interaction: discord.Interaction, *, data: str):
        """
        Calculate the Pearson correlation coefficient between two variables.
        Input should be pairs of x and y values.
        Example usage: /math correlation 1 2 2 4 3 6 4 8
        This would calculate correlation for points: (1,2), (2,4), (3,6), (4,8)
        """
        try:
            nums = [float(x) for x in data.split()]
            if len(nums) % 2 != 0:
                await interaction.response.send_message("Error: Please provide pairs of numbers (x y x y ...)")
                return
            x = nums[::2]  # Every other number starting from index 0
            y = nums[1::2]  # Every other number starting from index 1
            r = np.corrcoef(x, y)[0, 1]
            message = f"X values: {x}\nY values: {y}\nCorrelation coefficient (r) = {r:.4f}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="regression", description="Calculate linear regression (x y pairs)")
    async def regression(self, interaction: discord.Interaction, *, data: str):
        """
        Perform linear regression analysis on a set of (x,y) points.
        Calculates the line of best fit (y = mx + b) and R² value.
        Example usage: /math regression 1 2 2 4 3 6 4 8
        This would perform regression on points: (1,2), (2,4), (3,6), (4,8)
        """
        try:
            nums = [float(x) for x in data.split()]
            if len(nums) % 2 != 0:
                await interaction.response.send_message("Error: Please provide pairs of numbers (x y x y ...)")
                return
            x = np.array(nums[::2])  # Every other number starting from index 0
            y = np.array(nums[1::2])  # Every other number starting from index 1
            slope, intercept = np.polyfit(x, y, 1)
            r = np.corrcoef(x, y)[0, 1]
            r_squared = r ** 2
            
            message = f"Linear Regression Results:\n"
            message += f"Equation: y = {slope:.4f}x + {intercept:.4f}\n"
            message += f"R² (coefficient of determination) = {r_squared:.4f}\n"
            message += f"\nX values: {x.tolist()}\nY values: {y.tolist()}"
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="trig_solve", description="Solve triangle given side-angle pair")
    async def trig_solve(self, interaction: discord.Interaction, side: float, angle: float, is_opposite: bool):
        """
        Solve a right triangle given one side and one angle.
        Uses trigonometric ratios to find missing sides and angles.
        
        Args:
            side: Length of the known side
            angle: Known angle in degrees
            is_opposite: True if the known side is opposite to the known angle
        
        Example usage: /math trig_solve 5 30 true
        """
        try:
            if side <= 0 or angle <= 0 or angle >= 180:
                await interaction.response.send_message("Error: Invalid side length or angle")
                return
            
            angle_rad = math.radians(angle)
            if is_opposite:
                # Using law of sines to find other side
                other_side = side / math.sin(angle_rad)
                message = f"Given:\n- Side = {side}\n- Angle = {angle}°\n- Side is opposite to angle: {is_opposite}\n\n"
                message += f"Results:\n- Hypotenuse = {other_side:.4f}\n"
                message += f"- Other angle = {(90 - angle):.4f}°\n"
                message += f"- Other side = {(other_side * math.cos(angle_rad)):.4f}"
            else:
                # Using law of sines to find opposite side
                other_side = side * math.sin(angle_rad)
                message = f"Given:\n- Side = {side}\n- Angle = {angle}°\n- Side is adjacent to angle: {not is_opposite}\n\n"
                message += f"Results:\n- Opposite side = {other_side:.4f}\n"
                message += f"- Other angle = {(90 - angle):.4f}°\n"
                message += f"- Hypotenuse = {(side / math.cos(angle_rad)):.4f}"
            
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @math_group.command(name="confidence_interval", description="Calculate confidence interval for mean")
    async def confidence_interval(self, interaction: discord.Interaction, confidence: float, *, numbers: str):
        """
        Calculate a confidence interval for the population mean.
        Uses Student's t-distribution for small sample sizes.
        
        Args:
            confidence: Confidence level (0-100)
            numbers: Space-separated list of sample values
        
        Example usage: /math confidence_interval 95 67 72 74 69 71 73
        This calculates a 95% confidence interval for the population mean
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await interaction.response.send_message("Error: Please provide numbers for the dataset")
                return
            if confidence <= 0 or confidence >= 100:
                await interaction.response.send_message("Error: Confidence level must be between 0 and 100")
                return
            
            data = np.array(nums)
            mean = np.mean(data)
            std_err = stats.sem(data)
            ci = stats.t.interval(confidence/100, len(data)-1, loc=mean, scale=std_err)
            
            message = f"Confidence Interval ({confidence}%):\n"
            message += f"Sample Mean = {mean:.4f}\n"
            message += f"Standard Error = {std_err:.4f}\n"
            message += f"Interval: ({ci[0]:.4f}, {ci[1]:.4f})\n"
            message += f"\nDataset: {nums}"
            
            await send_long_message(interaction, message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    """Register the Math cog with the bot."""
    await bot.add_cog(Math(bot))
