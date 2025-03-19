"""
Math Cog for Discord Bot
This module provides mathematical and statistical operations for AP PreCalc and AP Statistics.
It includes basic arithmetic, trigonometry, and statistical analysis functions.

Dependencies:
- numpy: For numerical computations and statistical functions
- scipy.stats: For advanced statistical operations
- math/cmath: For mathematical operations including complex numbers
"""

import discord
from discord.ext import commands
import math
import numpy as np
import sympy as sp
from scipy import stats
import textwrap
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get guild IDs from environment variable
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

async def send_long_message(ctx, content: str):
    """
    Utility function to send messages that might exceed Discord's 2000 character limit.
    Splits long messages into chunks and sends them sequentially.
    
    Args:
        ctx: Discord application context object
        content: The message content to send
    """
    if len(content) <= 2000:
        await ctx.respond(content)
        return

    chunks = textwrap.wrap(content, width=1990, replace_whitespace=False)
    await ctx.respond(chunks[0])

    for chunk in chunks[1:]:
        await ctx.send_followup(chunk)

class Math(commands.Cog):
    """
    A cog that provides mathematical and statistical operations through Discord slash commands.
    Includes functionality for both AP PreCalc and AP Statistics coursework.
    """
    
    def __init__(self, bot):
        """
        Initialize the Math Cog.
        
        Args:
            bot (commands.Bot): The bot instance
        """
        self.bot = bot
        
        # Create the command group within the class
        self.math_group = bot.create_group(name="math", description="Advanced mathematical operations")

        # Dynamically add commands to the group
        self.math_group.command(name="add", description="Add two numbers", guild_ids=GUILD_IDS)(self.add)
        self.math_group.command(name="subtract", description="Subtract two numbers", guild_ids=GUILD_IDS)(self.subtract)
        self.math_group.command(name="multiply", description="Multiply two numbers", guild_ids=GUILD_IDS)(self.multiply)
        self.math_group.command(name="divide", description="Divide two numbers", guild_ids=GUILD_IDS)(self.divide)
        self.math_group.command(name="power", description="Calculate a number raised to a power", guild_ids=GUILD_IDS)(self.power)
        self.math_group.command(name="sqrt", description="Calculate the square root of a number", guild_ids=GUILD_IDS)(self.sqrt)
        self.math_group.command(name="sin", description="Calculate sine (in degrees)", guild_ids=GUILD_IDS)(self.sin)
        self.math_group.command(name="cos", description="Calculate cosine (in degrees)", guild_ids=GUILD_IDS)(self.cos)
        self.math_group.command(name="tan", description="Calculate tangent (in degrees)", guild_ids=GUILD_IDS)(self.tan)
        self.math_group.command(name="log", description="Calculate logarithm with custom base", guild_ids=GUILD_IDS)(self.log)
        self.math_group.command(name="ln", description="Calculate natural logarithm", guild_ids=GUILD_IDS)(self.ln)
        self.math_group.command(name="area_circle", description="Calculate area of a circle", guild_ids=GUILD_IDS)(self.area_circle)
        self.math_group.command(name="area_triangle", description="Calculate area of a triangle using base and height", guild_ids=GUILD_IDS)(self.area_triangle)
        self.math_group.command(name="mean", description="Calculate arithmetic mean of numbers (separate with spaces)", guild_ids=GUILD_IDS)(self.mean)
        self.math_group.command(name="quadratic", description="Solve quadratic equation ax² + bx + c = 0", guild_ids=GUILD_IDS)(self.quadratic)
        self.math_group.command(name="median", description="Calculate median of numbers (separate with spaces)", guild_ids=GUILD_IDS)(self.median)
        self.math_group.command(name="mode", description="Calculate mode of numbers (separate with spaces)", guild_ids=GUILD_IDS)(self.mode)
        self.math_group.command(name="std_dev", description="Calculate standard deviation (separate numbers with spaces)", guild_ids=GUILD_IDS)(self.std_dev)
        self.math_group.command(name="variance", description="Calculate variance (separate numbers with spaces)", guild_ids=GUILD_IDS)(self.variance)
        self.math_group.command(name="z_score", description="Calculate z-score for a value in a dataset", guild_ids=GUILD_IDS)(self.z_score)
        self.math_group.command(name="correlation", description="Calculate Pearson correlation coefficient (x y pairs)", guild_ids=GUILD_IDS)(self.correlation)
        self.math_group.command(name="regression", description="Calculate linear regression (x y pairs)", guild_ids=GUILD_IDS)(self.regression)
        self.math_group.command(name="trig_solve", description="Solve triangle given side-angle pair", guild_ids=GUILD_IDS)(self.trig_solve)
        self.math_group.command(name="confidence_interval", description="Calculate confidence interval for mean", guild_ids=GUILD_IDS)(self.confidence_interval)

    async def add(self, ctx, num1: float, num2: float):
        """
        Add two numbers together.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 + num2
            await ctx.respond(f"{num1} + {num2} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def subtract(self, ctx, num1: float, num2: float):
        """
        Subtract the second number from the first.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 - num2
            await ctx.respond(f"{num1} - {num2} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def multiply(self, ctx, num1: float, num2: float):
        """
        Multiply two numbers together.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            num1: The first number
            num2: The second number
        """
        try:
            result = num1 * num2
            await ctx.respond(f"{num1} × {num2} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def divide(self, ctx, num1: float, num2: float):
        """
        Divide the first number by the second.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            num1: The dividend
            num2: The divisor
        """
        try:
            if num2 == 0:
                await ctx.respond("Cannot divide by zero!")
                return
            result = num1 / num2
            await ctx.respond(f"{num1} ÷ {num2} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def power(self, ctx, base: float, exponent: float):
        """
        Calculate the result of raising a number to a power.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            base: The base number
            exponent: The exponent
        """
        try:
            result = math.pow(base, exponent)
            await ctx.respond(f"{base}^{exponent} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def sqrt(self, ctx, number: float):
        """
        Calculate the square root of a number.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            number: The number to find the square root of
        """
        try:
            if number < 0:
                result = cmath.sqrt(number)
                await ctx.respond(f"√{number} = {result} (complex number)")
            else:
                result = math.sqrt(number)
                await ctx.respond(f"√{number} = {result}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def sin(self, ctx, angle: float):
        """
        Calculate the sine of an angle in degrees.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            angle: The angle in degrees
        """
        try:
            result = math.sin(math.radians(angle))
            await ctx.respond(f"sin({angle}°) = {result:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def cos(self, ctx, angle: float):
        """
        Calculate the cosine of an angle in degrees.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            angle: The angle in degrees
        """
        try:
            result = math.cos(math.radians(angle))
            await ctx.respond(f"cos({angle}°) = {result:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def tan(self, ctx, angle: float):
        """
        Calculate the tangent of an angle in degrees.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            angle: The angle in degrees
        """
        try:
            if abs(math.cos(math.radians(angle))) < 1e-10:
                await ctx.respond("Error: tangent is undefined at this angle")
                return
            result = math.tan(math.radians(angle))
            await ctx.respond(f"tan({angle}°) = {result:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def log(self, ctx, number: float, base: float | None = None):
        """
        Calculate the logarithm of a number with a custom base.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            number: The number to find the logarithm of
            base: The base of the logarithm (default is 10)
        """
        try:
            if base is None:
                base = 10.0
            if number <= 0 or base <= 0 or base == 1:
                await ctx.respond("Error: Invalid input for logarithm")
                return
            result = math.log(number, base)
            await ctx.respond(f"log_{base}({number}) = {result:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def ln(self, ctx, number: float):
        """
        Calculate the natural logarithm of a number.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            number: The number to find the natural logarithm of
        """
        try:
            if number <= 0:
                await ctx.respond("Error: Cannot calculate natural logarithm of non-positive number")
                return
            result = math.log(number)
            await ctx.respond(f"ln({number}) = {result:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def area_circle(self, ctx, radius: float):
        """
        Calculate the area of a circle.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            radius: The radius of the circle
        """
        try:
            if radius < 0:
                await ctx.respond("Error: Radius cannot be negative")
                return
            area = math.pi * radius * radius
            await ctx.respond(f"Area of circle with radius {radius} = {area:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def area_triangle(self, ctx, base: float, height: float):
        """
        Calculate the area of a triangle using the base and height.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            base: The base of the triangle
            height: The height of the triangle
        """
        try:
            if base < 0 or height < 0:
                await ctx.respond("Error: Dimensions cannot be negative")
                return
            area = 0.5 * base * height
            await ctx.respond(f"Area of triangle with base {base} and height {height} = {area:.4f}")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def mean(self, ctx, *, numbers: str):
        """
        Calculate the arithmetic mean of a set of numbers.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            numbers: Space-separated list of numbers
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers to calculate mean")
                return
            result = sum(nums) / len(nums)
            message = f"Numbers provided: {nums}\nMean = {result:.4f}\n"
            message += f"\nDetailed calculation:\nSum = {sum(nums)}\nCount = {len(nums)}\nMean = Sum/Count = {result:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def quadratic(self, ctx, a: float, b: float, c: float):
        """
        Solve a quadratic equation of the form ax² + bx + c = 0.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            a: The coefficient of the squared term
            b: The coefficient of the linear term
            c: The constant term
        """
        try:
            if a == 0:
                await ctx.respond("Error: Not a quadratic equation (a = 0)")
                return
            
            discriminant = b**2 - 4*a*c
            
            if discriminant > 0:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                await ctx.respond(f"Two real solutions:\nx₁ = {x1:.4f}\nx₂ = {x2:.4f}")
            elif discriminant == 0:
                x = -b / (2*a)
                await ctx.respond(f"One real solution:\nx = {x:.4f}")
            else:
                real = -b / (2*a)
                imag = math.sqrt(-discriminant) / (2*a)
                await ctx.respond(
                    f"Two complex solutions:\n"
                    f"x₁ = {real:.4f} + {imag:.4f}i\n"
                    f"x₂ = {real:.4f} - {imag:.4f}i"
                )
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def median(self, ctx, *, numbers: str):
        """
        Calculate the median (middle value) of a dataset.
        Example usage: /math median 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers to calculate median")
                return
            result = np.median(nums)
            message = f"Numbers provided: {nums}\nMedian = {result:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def mode(self, ctx, *, numbers: str):
        """
        Find the mode (most frequent value) in a dataset.
        Example usage: /math mode 1 2 2 3 3 3 4
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers to calculate mode")
                return
            mode_result = stats.mode(nums)
            message = f"Numbers provided: {nums}\nMode = {mode_result.mode[0]:.4f} (occurs {mode_result.count[0]} times)"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def std_dev(self, ctx, *, numbers: str):
        """
        Calculate the sample standard deviation of a dataset.
        Uses n-1 degrees of freedom (Bessel's correction).
        Example usage: /math std_dev 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers to calculate standard deviation")
                return
            result = np.std(nums, ddof=1)  # ddof=1 for sample standard deviation
            message = f"Numbers provided: {nums}\nStandard Deviation = {result:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def variance(self, ctx, *, numbers: str):
        """
        Calculate the sample variance of a dataset.
        Uses n-1 degrees of freedom (Bessel's correction).
        Example usage: /math variance 1 2 3 4 5
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers to calculate variance")
                return
            result = np.var(nums, ddof=1)  # ddof=1 for sample variance
            message = f"Numbers provided: {nums}\nVariance = {result:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def z_score(self, ctx, value: float, *, numbers: str):
        """
        Calculate the z-score (standard score) for a value within a dataset.
        Z-score represents how many standard deviations away from the mean a value is.
        Example usage: /math z_score 75 70 80 85 90 75 80
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide a dataset")
                return
            mean = np.mean(nums)
            std = np.std(nums, ddof=1)
            z = (value - mean) / std
            message = f"Value: {value}\nDataset: {nums}\nZ-score = {z:.4f}\n"
            message += f"\nCalculation details:\nMean = {mean:.4f}\nStandard Deviation = {std:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def correlation(self, ctx, *, data: str):
        """
        Calculate the Pearson correlation coefficient between two variables.
        Input should be pairs of x and y values.
        Example usage: /math correlation 1 2 2 4 3 6 4 8
        This would calculate correlation for points: (1,2), (2,4), (3,6), (4,8)
        """
        try:
            nums = [float(x) for x in data.split()]
            if len(nums) % 2 != 0:
                await ctx.respond("Error: Please provide pairs of numbers (x y x y ...)")
                return
            x = nums[::2]  # Every other number starting from index 0
            y = nums[1::2]  # Every other number starting from index 1
            r = np.corrcoef(x, y)[0, 1]
            message = f"X values: {x}\nY values: {y}\nCorrelation coefficient (r) = {r:.4f}"
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def regression(self, ctx, *, data: str):
        """
        Perform linear regression analysis on a set of (x,y) points.
        Calculates the line of best fit (y = mx + b) and R² value.
        Example usage: /math regression 1 2 2 4 3 6 4 8
        This would perform regression on points: (1,2), (2,4), (3,6), (4,8)
        """
        try:
            nums = [float(x) for x in data.split()]
            if len(nums) % 2 != 0:
                await ctx.respond("Error: Please provide pairs of numbers (x y x y ...)")
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
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def trig_solve(self, ctx, side: float, angle: float, is_opposite: bool):
        """
        Solve a right triangle given one side and one angle.
        Uses trigonometric ratios to find missing sides and angles.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            side: Length of the known side
            angle: Known angle in degrees
            is_opposite: True if the known side is opposite to the known angle
        
        Example usage: /math trig_solve 5 30 true
        """
        try:
            if side <= 0 or angle <= 0 or angle >= 180:
                await ctx.respond("Error: Invalid side length or angle")
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
            
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    async def confidence_interval(self, ctx, confidence: float, *, numbers: str):
        """
        Calculate a confidence interval for the population mean.
        Uses Student's t-distribution for small sample sizes.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            confidence: Confidence level (0-100)
            numbers: Space-separated list of sample values
        
        Example usage: /math confidence_interval 95 67 72 74 69 71 73
        This calculates a 95% confidence interval for the population mean
        """
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                await ctx.respond("Error: Please provide numbers for the dataset")
                return
            if confidence <= 0 or confidence >= 100:
                await ctx.respond("Error: Confidence level must be between 0 and 100")
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
            
            await send_long_message(ctx, message)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @discord.slash_command()
    async def solve_equation(self, ctx, equation: str):
        """
        Solve a mathematical equation symbolically.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            equation (str): The equation to solve
        """
        try:
            # Use SymPy to solve the equation
            x = sp.Symbol('x')
            solution = sp.solve(sp.sympify(equation), x)
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Equation Solver",
                description=f"Solving: {equation}",
                color=discord.Color.purple()
            )
            
            # Add solution(s) to the embed
            if solution:
                for i, sol in enumerate(solution, 1):
                    embed.add_field(
                        name=f"Solution {i}", 
                        value=str(sol), 
                        inline=False
                    )
            else:
                embed.add_field(
                    name="Result", 
                    value="No real solutions found", 
                    inline=False
                )
            
            await ctx.respond(embed=embed)
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @discord.slash_command()
    async def statistical_analysis(self, ctx, data: str):
        """
        Perform statistical analysis on a list of numbers.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            data (str): Comma-separated list of numbers
        """
        try:
            # Convert input string to list of floats
            numbers = [float(x.strip()) for x in data.split(',')]
            
            # Calculate statistical metrics
            mean = np.mean(numbers)
            median = np.median(numbers)
            std_dev = np.std(numbers)
            variance = np.var(numbers)
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Statistical Analysis",
                description=f"Analysis of: {data}",
                color=discord.Color.green()
            )
            embed.add_field(name="Mean", value=f"{mean:.2f}", inline=False)
            embed.add_field(name="Median", value=f"{median:.2f}", inline=False)
            embed.add_field(name="Standard Deviation", value=f"{std_dev:.2f}", inline=False)
            embed.add_field(name="Variance", value=f"{variance:.2f}", inline=False)
            
            await ctx.respond(embed=embed)
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @discord.slash_command()
    async def probability_distribution(self, ctx, distribution: str, *params):
        """
        Calculate probability distribution metrics.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            distribution (str): Type of distribution (normal, binomial, poisson)
            params (float): Distribution parameters
        """
        try:
            # Convert params to floats
            params = [float(p) for p in params]
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Probability Distribution",
                description=f"Distribution: {distribution.capitalize()}",
                color=discord.Color.blue()
            )
            
            # Calculate distribution-specific metrics
            if distribution.lower() == 'normal':
                # Expects mean and standard deviation
                if len(params) != 2:
                    raise ValueError("Normal distribution requires mean and standard deviation")
                mean, std = params
                
                # Calculate probability density at mean
                pdf_at_mean = stats.norm.pdf(mean, mean, std)
                
                embed.add_field(name="Mean", value=f"{mean}", inline=False)
                embed.add_field(name="Standard Deviation", value=f"{std}", inline=False)
                embed.add_field(name="PDF at Mean", value=f"{pdf_at_mean:.4f}", inline=False)
            
            elif distribution.lower() == 'binomial':
                # Expects n (trials) and p (probability of success)
                if len(params) != 2:
                    raise ValueError("Binomial distribution requires number of trials and probability")
                n, p = params
                
                # Calculate mean and variance
                binom_mean = n * p
                binom_var = n * p * (1 - p)
                
                embed.add_field(name="Trials", value=f"{n}", inline=False)
                embed.add_field(name="Probability of Success", value=f"{p}", inline=False)
                embed.add_field(name="Mean", value=f"{binom_mean}", inline=False)
                embed.add_field(name="Variance", value=f"{binom_var}", inline=False)
            
            elif distribution.lower() == 'poisson':
                # Expects lambda (average rate)
                if len(params) != 1:
                    raise ValueError("Poisson distribution requires average rate")
                lam = params[0]
                
                # Calculate mean and variance
                poisson_mean = lam
                poisson_var = lam
                
                embed.add_field(name="Average Rate", value=f"{lam}", inline=False)
                embed.add_field(name="Mean", value=f"{poisson_mean}", inline=False)
                embed.add_field(name="Variance", value=f"{poisson_var}", inline=False)
            
            else:
                raise ValueError("Unsupported distribution type")
            
            await ctx.respond(embed=embed)
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

def setup(bot):
    """
    Set up the Math Cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    pass  # Cog is now added in Main.py __init__ method
