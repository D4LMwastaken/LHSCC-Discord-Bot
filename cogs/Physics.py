"""
Physics Cog for Discord Bot
This module provides physics calculations and formulas for AP Physics 1.
Covers topics including kinematics, forces, energy, momentum, and rotational motion.
"""

import discord
from discord.ext import commands
import math
import numpy as np
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get guild IDs from environment variable
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('GUILD_IDS', '').split(',') if guild_id.strip()]

class Physics(commands.Cog):
    """
    A cog that provides physics calculations through Discord slash commands.
    Focuses on AP Physics 1 topics.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kinematics", guild_ids=GUILD_IDS)
    async def kinematics(self, ctx, 
                         initial_velocity: Optional[float] = 0, 
                         final_velocity: Optional[float] = 0, 
                         acceleration: Optional[float] = 0, 
                         time: Optional[float] = 0, 
                         displacement: Optional[float] = 0):
        """
        Calculate kinematics parameters.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            initial_velocity (Optional[float]): Initial velocity in m/s
            final_velocity (Optional[float]): Final velocity in m/s
            acceleration (Optional[float]): Acceleration in m/s²
            time (Optional[float]): Time in seconds
            displacement (Optional[float]): Displacement in meters
        """
        await ctx.defer()
        try:
            # Kinematics calculations using provided parameters
            result = calculate_kinematics(
                initial_velocity, final_velocity, 
                acceleration, time, displacement
            )
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Kinematics Calculation Results", 
                color=discord.Color.blue()
            )
            
            for key, value in result.items():
                embed.add_field(name=key, value=f"{value:.2f}", inline=False)
            
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="forces", guild_ids=GUILD_IDS)
    async def force(self, ctx, mass: float, acceleration: float):
        """
        Calculate force using Newton's Second Law.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            mass (float): Mass of the object in kg
            acceleration (float): Acceleration in m/s²
        """
        await ctx.defer()
        try:
            force = mass * acceleration
            await ctx.respond(f"Force = {force:.2f} N (Mass: {mass} kg, Acceleration: {acceleration} m/s²)")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="energy", guild_ids=GUILD_IDS)
    async def energy(self, ctx, mass: float, height: Optional[float] = None, velocity: Optional[float] = None):
        """
        Calculate potential or kinetic energy.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            mass (float): Mass of the object in kg
            height (Optional[float]): Height in meters for potential energy
            velocity (Optional[float]): Velocity in m/s for kinetic energy
        """
        await ctx.defer()
        try:
            # Gravitational acceleration constant
            g = 9.8  # m/s²
            
            # Calculate potential energy if height is provided
            if height is not None:
                potential_energy = mass * g * height
                await ctx.respond(f"Potential Energy = {potential_energy:.2f} J (Mass: {mass} kg, Height: {height} m)")
            
            # Calculate kinetic energy if velocity is provided
            elif velocity is not None:
                kinetic_energy = 0.5 * mass * (velocity ** 2)
                await ctx.respond(f"Kinetic Energy = {kinetic_energy:.2f} J (Mass: {mass} kg, Velocity: {velocity} m/s)")
            
            else:
                await ctx.respond("Please provide either height or velocity to calculate energy.")
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="momentum", guild_ids=GUILD_IDS)
    async def momentum(self, ctx, mass: float, velocity: float):
        """
        Calculate momentum.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            mass (float): Mass of the object in kg
            velocity (float): Velocity of the object in m/s
        """
        await ctx.defer()
        try:
            mom = mass * velocity
            await ctx.respond(f"Momentum = {mom:.2f} kg⋅m/s (Mass: {mass} kg, Velocity: {velocity} m/s)")
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="rotation", guild_ids=GUILD_IDS)
    async def rotation(self, ctx, torque: Optional[float] = None, moment_of_inertia: Optional[float] = None, angular_acceleration: Optional[float] = None):
        """
        Calculate rotational motion parameters.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            torque (Optional[float]): Torque in N⋅m
            moment_of_inertia (Optional[float]): Moment of inertia in kg⋅m²
            angular_acceleration (Optional[float]): Angular acceleration in rad/s²
        """
        await ctx.defer()
        try:
            # Torque = Moment of Inertia * Angular Acceleration
            if torque is not None and moment_of_inertia is not None:
                calculated_angular_acceleration = torque / moment_of_inertia
                await ctx.respond(f"Angular Acceleration = {calculated_angular_acceleration:.2f} rad/s² (Torque: {torque} N⋅m, Moment of Inertia: {moment_of_inertia} kg⋅m²)")
            
            elif moment_of_inertia is not None and angular_acceleration is not None and torque is None:
                calculated_torque = moment_of_inertia * angular_acceleration
                await ctx.respond(f"Torque = {calculated_torque:.2f} N⋅m (Moment of Inertia: {moment_of_inertia} kg⋅m², Angular Acceleration: {angular_acceleration} rad/s²)")
            
            else:
                await ctx.respond("Please provide sufficient parameters to calculate rotational motion.")
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="projectile_motion", description="Calculate projectile motion parameters", guild_ids=GUILD_IDS)
    async def projectile_motion(
        self, 
        ctx, 
        initial_velocity: float, 
        angle: float, 
        height: float = 0
    ):
        """
        Calculate projectile motion parameters.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            initial_velocity: Initial velocity in m/s
            angle: Launch angle in degrees
            height: Initial height in meters. Defaults to 0.
        """
        try:
            # Convert angle to radians
            angle_rad = math.radians(angle)
            
            # Calculate horizontal and vertical components of velocity
            v0x = initial_velocity * math.cos(angle_rad)
            v0y = initial_velocity * math.sin(angle_rad)
            
            # Calculate time of flight
            # Using quadratic formula for time with initial height
            g = 9.8  # Acceleration due to gravity
            time_of_flight = (v0y + math.sqrt(v0y**2 + 2*g*height)) / g
            
            # Calculate maximum height
            max_height = height + (v0y**2 / (2*g))
            
            # Calculate horizontal range
            range_distance = v0x * time_of_flight
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Projectile Motion Calculation",
                color=discord.Color.blue()
            )
            embed.add_field(name="Initial Velocity", value=f"{initial_velocity} m/s", inline=False)
            embed.add_field(name="Launch Angle", value=f"{angle}°", inline=False)
            embed.add_field(name="Initial Height", value=f"{height} m", inline=False)
            embed.add_field(name="Time of Flight", value=f"{time_of_flight:.2f} s", inline=False)
            embed.add_field(name="Maximum Height", value=f"{max_height:.2f} m", inline=False)
            embed.add_field(name="Horizontal Range", value=f"{range_distance:.2f} m", inline=False)
            
            await ctx.respond(embed=embed)
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

    @commands.slash_command(name="pendulum_period", description="Calculate pendulum period", guild_ids=GUILD_IDS)
    async def pendulum_period(
        self, 
        ctx, 
        length: float
    ):
        """
        Calculate the period of a simple pendulum.
        
        Args:
            ctx (discord.ApplicationContext): The context of the interaction
            length: Length of the pendulum in meters
        """
        try:
            # Gravitational acceleration constant
            g = 9.8
            
            # Calculate period using simple pendulum formula
            period = 2 * math.pi * math.sqrt(length / g)
            
            # Create an embed to display results
            embed = discord.Embed(
                title="Simple Pendulum Period Calculation",
                color=discord.Color.green()
            )
            embed.add_field(name="Pendulum Length", value=f"{length} m", inline=False)
            embed.add_field(name="Gravitational Acceleration", value=f"{g} m/s²", inline=False)
            embed.add_field(name="Pendulum Period", value=f"{period:.2f} s", inline=False)
            
            await ctx.respond(embed=embed)
        
        except Exception as e:
            await ctx.respond(f"An error occurred: {str(e)}")

def setup(bot):
    """
    Set up the Physics Cog.
    
    Args:
        bot (commands.Bot): The bot instance
    """
    pass  # Cog is now added in Main.py __init__ method