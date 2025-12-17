using UnityEngine;
using UnityEngine.Events; // Necessário para criar eventos tipo "Ao Morrer"

public class HealthSystem : MonoBehaviour
{
    [Header("Configurações de Vida")]
    [SerializeField] private float maxHealth = 100f;
    private float currentHealth;

    [Header("Eventos de Combate")]
    public UnityEvent OnTakeDamage; // Dispara efeitos visuais/sons no Unity
    public UnityEvent OnDeath;      // Dispara lógica de Game Over ou Vitória

    private void Awake()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(float amount)
    {
        currentHealth -= amount;
        Debug.Log(gameObject.name + " recebeu dano! Vida: " + currentHealth);

        // Dispara o evento (ex: tocar som de dor, piscar em vermelho)
        OnTakeDamage?.Invoke();

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    private void Die()
    {
        Debug.Log(gameObject.name + " morreu!");
        OnDeath?.Invoke();
        
        // No Unity, desativamos o objeto ou tocamos animação de morte
        gameObject.SetActive(false); 
    }

    // Função útil para UI (Barra de Vida)
    public float GetHealthPercent()
    {
        return currentHealth / maxHealth;
    }
}