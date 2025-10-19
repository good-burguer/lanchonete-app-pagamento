from app.infrastructure.api.fastapi import app, Depends

from app.api import check
from app.api import pagamento
from app.webhooks import pagamento as pagamento_webhook

# declare
app.include_router(check.router)
app.include_router(pagamento.router)
app.include_router(pagamento_webhook.router)