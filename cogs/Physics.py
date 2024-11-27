"""
Physics Cog for Discord Bot
This module provides physics calculations and formulas for AP Physics 1.
Covers topics including kinematics, forces, energy, momentum, and rotational motion.
"""

import math
import discord
from discord import app_commands
from discord.ext import commands
import numpy as np

class Physics(commands.Cog):
    """
    A cog that provides physics calculations through Discord slash commands.
    Focuses on AP Physics 1 topics.
    """
    
    def __init__(self, bot):
        self.bot = bot

    physics_group = app_commands.Group(name="physics", description="Physics calculations and formulas")

    @physics_group.command(name="kinematics", description="Calculate kinematics values given initial conditions")
    async def kinematics(self, interaction: discord.Interaction, initial_velocity: float, 
                        acceleration: float, time: float):
        """
        Calculate displacement and final velocity using kinematics equations.
        Uses equations: v = v₀ + at, x = x₀ + v₀t + ½at²
        
        Args:
            initial_velocity: Initial velocity (m/s)
            acceleration: Acceleration (m/s²)
            time: Time interval (s)
        """
        try:
            final_velocity = initial_velocity + acceleration * time
            displacement = initial_velocity * time + 0.5 * acceleration * time * time
            
            message = "Kinematics Calculations:\n"
            message += f"Initial velocity (v₀) = {initial_velocity} m/s\n"
            message += f"Acceleration (a) = {acceleration} m/s²\n"
            message += f"Time (t) = {time} s\n\n"
            message += f"Results:\n"
            message += f"Final velocity (v) = {final_velocity:.2f} m/s\n"
            message += f"Displacement (Δx) = {displacement:.2f} m"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="force", description="Calculate net force and acceleration")
    async def force(self, interaction: discord.Interaction, mass: float, *forces: float):
        """
        Calculate net force and resulting acceleration using Newton's Second Law.
        
        Args:
            mass: Mass of the object (kg)
            *forces: Variable number of forces (N) to be summed
        """
        try:
            if not forces:
                await interaction.response.send_message("Error: Please provide at least one force")
                return
                
            net_force = sum(forces)
            acceleration = net_force / mass
            
            message = "Force Calculations:\n"
            message += f"Mass (m) = {mass} kg\n"
            message += f"Applied forces = {forces} N\n\n"
            message += f"Results:\n"
            message += f"Net force (F_net) = {net_force:.2f} N\n"
            message += f"Acceleration (a) = {acceleration:.2f} m/s²"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="energy", description="Calculate mechanical energy of a system")
    async def energy(self, interaction: discord.Interaction, mass: float, height: float, 
                    velocity: float, gravity: float = 9.81):
        """
        Calculate kinetic and potential energy of an object.
        
        Args:
            mass: Mass of the object (kg)
            height: Height above reference point (m)
            velocity: Velocity of the object (m/s)
            gravity: Acceleration due to gravity (m/s², default 9.81)
        """
        try:
            kinetic_energy = 0.5 * mass * velocity * velocity
            potential_energy = mass * gravity * height
            total_energy = kinetic_energy + potential_energy
            
            message = "Energy Calculations:\n"
            message += f"Mass (m) = {mass} kg\n"
            message += f"Height (h) = {height} m\n"
            message += f"Velocity (v) = {velocity} m/s\n"
            message += f"Gravity (g) = {gravity} m/s²\n\n"
            message += f"Results:\n"
            message += f"Kinetic Energy (KE) = {kinetic_energy:.2f} J\n"
            message += f"Potential Energy (PE) = {potential_energy:.2f} J\n"
            message += f"Total Mechanical Energy = {total_energy:.2f} J"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="momentum", description="Calculate momentum and impulse")
    async def momentum(self, interaction: discord.Interaction, mass: float, 
                      initial_velocity: float, final_velocity: float, time: float):
        """
        Calculate momentum change and impulse.
        
        Args:
            mass: Mass of the object (kg)
            initial_velocity: Initial velocity (m/s)
            final_velocity: Final velocity (m/s)
            time: Time interval (s)
        """
        try:
            initial_momentum = mass * initial_velocity
            final_momentum = mass * final_velocity
            momentum_change = final_momentum - initial_momentum
            impulse = momentum_change  # F*Δt = Δp
            average_force = impulse / time
            
            message = "Momentum and Impulse Calculations:\n"
            message += f"Mass (m) = {mass} kg\n"
            message += f"Initial velocity (v₁) = {initial_velocity} m/s\n"
            message += f"Final velocity (v₂) = {final_velocity} m/s\n"
            message += f"Time interval (Δt) = {time} s\n\n"
            message += f"Results:\n"
            message += f"Initial momentum (p₁) = {initial_momentum:.2f} kg⋅m/s\n"
            message += f"Final momentum (p₂) = {final_momentum:.2f} kg⋅m/s\n"
            message += f"Momentum change (Δp) = {momentum_change:.2f} kg⋅m/s\n"
            message += f"Impulse (J) = {impulse:.2f} N⋅s\n"
            message += f"Average force (F_avg) = {average_force:.2f} N"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="circular", description="Calculate centripetal acceleration and force")
    async def circular(self, interaction: discord.Interaction, mass: float, radius: float, 
                      velocity: float):
        """
        Calculate centripetal acceleration and force for circular motion.
        
        Args:
            mass: Mass of the object (kg)
            radius: Radius of circular path (m)
            velocity: Tangential velocity (m/s)
        """
        try:
            acceleration = (velocity * velocity) / radius
            force = mass * acceleration
            period = 2 * math.pi * radius / velocity
            frequency = 1 / period
            
            message = "Circular Motion Calculations:\n"
            message += f"Mass (m) = {mass} kg\n"
            message += f"Radius (r) = {radius} m\n"
            message += f"Velocity (v) = {velocity} m/s\n\n"
            message += f"Results:\n"
            message += f"Centripetal acceleration (a_c) = {acceleration:.2f} m/s²\n"
            message += f"Centripetal force (F_c) = {force:.2f} N\n"
            message += f"Period (T) = {period:.2f} s\n"
            message += f"Frequency (f) = {frequency:.2f} Hz"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="spring", description="Calculate spring force and energy")
    async def spring(self, interaction: discord.Interaction, spring_constant: float, 
                    displacement: float):
        """
        Calculate spring force and potential energy using Hooke's Law.
        
        Args:
            spring_constant: Spring constant k (N/m)
            displacement: Displacement from equilibrium (m)
        """
        try:
            force = -spring_constant * displacement  # Negative because it's a restoring force
            potential_energy = 0.5 * spring_constant * displacement * displacement
            
            message = "Spring Calculations:\n"
            message += f"Spring constant (k) = {spring_constant} N/m\n"
            message += f"Displacement (x) = {displacement} m\n\n"
            message += f"Results:\n"
            message += f"Spring force (F) = {force:.2f} N\n"
            message += f"Spring potential energy (U) = {potential_energy:.2f} J"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @physics_group.command(name="rotation", description="Calculate rotational motion values")
    async def rotation(self, interaction: discord.Interaction, moment_of_inertia: float, 
                      angular_velocity: float, radius: float):
        """
        Calculate rotational kinetic energy and angular momentum.
        
        Args:
            moment_of_inertia: Moment of inertia (kg⋅m²)
            angular_velocity: Angular velocity (rad/s)
            radius: Distance from rotation axis (m)
        """
        try:
            rotational_ke = 0.5 * moment_of_inertia * angular_velocity * angular_velocity
            angular_momentum = moment_of_inertia * angular_velocity
            tangential_velocity = angular_velocity * radius
            
            message = "Rotational Motion Calculations:\n"
            message += f"Moment of inertia (I) = {moment_of_inertia} kg⋅m²\n"
            message += f"Angular velocity (ω) = {angular_velocity} rad/s\n"
            message += f"Radius (r) = {radius} m\n\n"
            message += f"Results:\n"
            message += f"Rotational kinetic energy = {rotational_ke:.2f} J\n"
            message += f"Angular momentum (L) = {angular_momentum:.2f} kg⋅m²/s\n"
            message += f"Tangential velocity (v) = {tangential_velocity:.2f} m/s"
            
            await interaction.response.send_message(message)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    """Register the Physics cog with the bot."""
    await bot.add_cog(Physics(bot))