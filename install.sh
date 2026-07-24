#!/bin/bash
echo "Installing Travel Agent dependencies..."
pip install -r requirements.txt
echo ""
echo "Installation complete!"
echo ""
echo "To run the Travel Agent API:"
echo "  uvicorn main:app --reload"
echo ""