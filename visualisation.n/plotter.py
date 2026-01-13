import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
from entities.body import MaterialBody
from fields.velocity_field import VelocityField


class Plotter:
    """Класс для визуализации результатов"""

    @staticmethod
    def plot_trajectories(body: MaterialBody, save_path: str = None):
        """Строит графики траекторий всех точек тела"""
        plt.figure(figsize=(10, 8))

        for trajectory in body.trajectories:
            x_vals, y_vals = trajectory.get_coordinates()
            plt.plot(x_vals, y_vals, 'b-', alpha=0.5, linewidth=0.5)

        # Начальная и конечная формы
        x_init, y_init = body.get_initial_shape()
        x_curr, y_curr = body.get_current_shape()

        plt.plot(x_init, y_init, 'ro-', label='Начальная форма', markersize=3)
        plt.plot(x_curr, y_curr, 'go-', label='Конечная форма', markersize=3)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Траектории движения материальных точек')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

    @staticmethod
    def plot_body_shapes(body: MaterialBody, save_path: str = None):
        """Сравнивает начальную и деформированную формы тела"""
        plt.figure(figsize=(12, 5))

        # Начальная форма
        plt.subplot(1, 2, 1)
        x_init, y_init = body.get_initial_shape()
        plt.plot(x_init, y_init, 'bo-')
        plt.fill(x_init, y_init, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Начальная форма тела')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

        # Деформированная форма
        plt.subplot(1, 2, 2)
        x_curr, y_curr = body.get_current_shape()
        plt.plot(x_curr, y_curr, 'ro-')
        plt.fill(x_curr, y_curr, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Деформированная форма тела')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

    @staticmethod
    def plot_velocity_fields(velocity_field: VelocityField,
                             times: List[float],
                             x_range: Tuple[float, float],
                             y_range: Tuple[float, float],
                             save_path: str = None):
        """Строит поля распределения скоростей и линии тока"""
        n_times = len(times)
        fig, axes = plt.subplots(n_times, 2, figsize=(15, 5 * n_times))

        if n_times == 1:
            axes = axes.reshape(1, -1)

        for idx, t in enumerate(times):
            # Поле скоростей
            X, Y, U, V = velocity_field.generate_streamlines(x_range, y_range, t)

            ax1 = axes[idx, 0]
            speed = np.sqrt(U ** 2 + V ** 2)
            contour = ax1.contourf(X, Y, speed, cmap='viridis', alpha=0.8)
            ax1.streamplot(X, Y, U, V, color='white', linewidth=0.5, density=2)
            plt.colorbar(contour, ax=ax1)
            ax1.set_xlabel('x')
            ax1.set_ylabel('y')
            ax1.set_title(f'Поле скоростей при t = {t:.2f}')
            ax1.grid(True, alpha=0.3)
            ax1.axis('equal')

            # Линии тока
            ax2 = axes[idx, 1]
            ax2.streamplot(X, Y, U, V, color='blue', linewidth=1, density=2)
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_title(f'Линии тока при t = {t:.2f}')
            ax2.grid(True, alpha=0.3)
            ax2.axis('equal')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()