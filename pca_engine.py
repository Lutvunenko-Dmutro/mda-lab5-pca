import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class PCAAnalyzer:
    def __init__(self, dataframe):
        self.raw_data = dataframe
        self.scaler = StandardScaler()
        self.pca = None
        self.scaled_data = None
        
    def run_analysis(self):
        # 1. Стандартизація
        self.scaled_data = self.scaler.fit_transform(self.raw_data)
        
        # 2. PCA (беремо всі компоненти для аналізу)
        n_cols = self.raw_data.shape[1]
        self.pca = PCA(n_components=n_cols)
        principal_components = self.pca.fit_transform(self.scaled_data)
        
        # DataFrame з результатами (Значення факторів для підприємств)
        col_names = [f'Фактор {i+1}' for i in range(n_cols)]
        self.results_df = pd.DataFrame(
            data=principal_components,
            columns=col_names,
            index=self.raw_data.index
        )
        self.results_df.index.name = '№ Підприємства'
        
        # 3. Факторні навантаження (Factor Loadings)
        # Формула: Eigenvectors * sqrt(Eigenvalues)
        loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        
        self.loadings_df = pd.DataFrame(
            data=loadings,
            columns=col_names,
            index=self.raw_data.columns
        )

    def get_explained_variance(self):
        """Повертає відсоток інформації, яку несе кожен фактор"""
        return pd.DataFrame({
            'Фактор': [f'Фактор {i+1}' for i in range(len(self.pca.explained_variance_ratio_))],
            'Дисперсія (%)': self.pca.explained_variance_ratio_ * 100
        })